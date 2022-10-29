## 1. Define a ColumnData representing any TableStore object.

```Java
import com.alibaba.fastjson.JSONObject;

import java.io.Serializable;

/**
 * 列式数据的抽象 <br>
 * 参考： https://help.aliyun.com/document_detail/43013.html
 *
 * @author David Euler
 * @created 2022/1/05
 */
public interface ColumnData extends Serializable {

    /**
     * 获取 OTS表 的主键列名称
     * @return
     */
    String[] getPrimaryKeyNames();

    /**
     * 对应的 ots 表名称
     * @return
     */
    String getTableName();

    /**
     * @return 返回数据库表的多元索引名称
     */
    String getDefaultSearchIndexName();


    default String toJsonString() {
        return JSONObject.toJSONString(this);
    }

    default JSONObject toJSONObject() {
        return JSONObject.parseObject(this.toJsonString());
    }
}

```

## 2. Implement general tablestore access class

Implement common method to put, get, update, delete data.

```Java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

import com.alicloud.openservices.tablestore.SyncClient;
import com.alicloud.openservices.tablestore.model.Column;
import com.alicloud.openservices.tablestore.model.ColumnValue;
import com.alicloud.openservices.tablestore.model.DeleteRowRequest;
import com.alicloud.openservices.tablestore.model.GetRowRequest;
import com.alicloud.openservices.tablestore.model.GetRowResponse;
import com.alicloud.openservices.tablestore.model.PrimaryKey;
import com.alicloud.openservices.tablestore.model.PrimaryKeyBuilder;
import com.alicloud.openservices.tablestore.model.PrimaryKeyValue;
import com.alicloud.openservices.tablestore.model.PutRowRequest;
import com.alicloud.openservices.tablestore.model.Row;
import com.alicloud.openservices.tablestore.model.RowDeleteChange;
import com.alicloud.openservices.tablestore.model.RowPutChange;
import com.alicloud.openservices.tablestore.model.RowUpdateChange;
import com.alicloud.openservices.tablestore.model.SingleRowQueryCriteria;
import com.alicloud.openservices.tablestore.model.UpdateRowRequest;
import com.alicloud.openservices.tablestore.model.search.SearchQuery;
import com.alicloud.openservices.tablestore.model.search.SearchRequest;
import com.alicloud.openservices.tablestore.model.search.SearchResponse;
import com.alicloud.openservices.tablestore.model.search.query.BoolQuery;
import com.alicloud.openservices.tablestore.model.search.query.Query;
import com.google.common.base.Preconditions;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.FatalBeanException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ResolvableType;
import org.springframework.util.CollectionUtils;

import java.beans.PropertyDescriptor;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.lang.reflect.ParameterizedType;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * OTS 数据存储类
 *
 * @author David Euler
 * @created 2022/01/05
 */
@Slf4j
public class DataMapper<T extends ColumnData> {

    public static final List<String> EMPTY_LIST = new ArrayList<>();

    protected Class<T> clazz;

    @Autowired
    protected SyncClient client;

    public DataMapper(){
        this.clazz = (Class<T>) ((ParameterizedType) getClass().getGenericSuperclass()).getActualTypeArguments()[0];
    }

    /** 子类可以设置要忽略的，对应  Bean 中不需要从 OTS 中获取的字段名列表  */
    public List<String> getIgnoreList() {return EMPTY_LIST;}

    /**
     * 默认的 readRowData() 实现， 各个子类可以根据需要各自实现 readRowData() 方法
     * @param row
     * @return
     */
    public T readRowData(Row row) {
        if (null == row) {
            return null;
        }

        try {
            T targetBean = clazz.getDeclaredConstructor().newInstance();

            // Step 1. 获取 Bean 的所有属性
            PropertyDescriptor[] targetPds = BeanUtils.getPropertyDescriptors(clazz);

            for (PropertyDescriptor targetPd : targetPds) {
                Method writeMethod = targetPd.getWriteMethod();
                List<String> ignoreList = getIgnoreList();

                // Step 2. 调用属性的写入方法，设置值
                if (writeMethod != null && (ignoreList == null || !ignoreList.contains(targetPd.getName()))) {

                    ResolvableType targetResolvableType = ResolvableType.forMethodParameter(writeMethod, 0);

                    // 根据 setXxx() 的参数类型，判断要从 Row Column 中获取的字段类型
                    Object value = null;
                    // Long
                    if (targetResolvableType.getType().getTypeName().equals(Long.class.getTypeName())) {
                        value = OTSFileObjectDatabase.getColumnValueAsLong(targetPd.getName(), row);
                    } else if (targetResolvableType.getType().getTypeName().equals(Boolean.class.getTypeName())) {
                        value = OTSFileObjectDatabase.getColumnValueAsBoolean(targetPd.getName(), row);
                    } else if (targetResolvableType.getType().getTypeName().equals(String.class.getTypeName())) {
                        value = OTSFileObjectDatabase.getColumnValueAsString(targetPd.getName(), row);
                    } else {
                        log.warn("Bean property type could not be resolved! class:{} property:{}",
                            targetBean.getClass().getSimpleName(), targetPd.getName());
                    }
                    if (null == value) {
                        log.warn("Bean property is null, it shall not occur! class:{} property:{}",
                            targetBean.getClass().getSimpleName(), targetPd.getName());
                    }

                    try {
                        if (!Modifier.isPublic(writeMethod.getDeclaringClass().getModifiers())) {
                            writeMethod.setAccessible(true);
                        }

                        writeMethod.invoke(targetBean, value);
                    } catch (Throwable var18) {
                        throw new FatalBeanException(
                            "Could not copy property '" + targetPd.getName() + "' from source to target", var18);
                    }

                }
            }

            return targetBean;

        } catch (Exception e) {
            String msg = "Failed to readRowData for class:" + clazz.getSimpleName();
            log.error(msg, e);
            throw new RuntimeException(e);
        }
    }

    /**
     * 添加一条数据
     * <p>
     * 参考： https://help.aliyun.com/document_detail/43013.html
     *
     * @param columnData
     */
    public void putRow(T columnData) {

        JSONObject jsonObject = columnData.toJSONObject();

        PrimaryKey primaryKey = getPrimaryKeyAndRemovePkFromObject(columnData.getPrimaryKeyNames(), jsonObject);

        //设置数据表名称。
        RowPutChange rowPutChange = new RowPutChange(columnData.getTableName(), primaryKey);

        //属性字段，保存到 OTS 的属性列中
        for (String columnName : jsonObject.keySet()) {
            Object columnValue = jsonObject.get(columnName);

            Column column = buildColumn(columnName, columnValue);

            rowPutChange.addColumn(column);
        }

        client.putRow(new PutRowRequest(rowPutChange));
    }

    /**
     * 更新一行数据
     *
     * @param columnData
     */
    public void updateRow(T columnData) {

        JSONObject jsonObject = columnData.toJSONObject();

        PrimaryKey primaryKey = getPrimaryKeyAndRemovePkFromObject(columnData.getPrimaryKeyNames(), jsonObject);

        //设置数据表名称。
        RowUpdateChange rowUpdateChange = new RowUpdateChange(columnData.getTableName(), primaryKey);

        //属性字段，保存到 OTS 的属性列中
        for (String columnName : jsonObject.keySet()) {
            Object columnValue = jsonObject.get(columnName);
            Column column = buildColumn(columnName, columnValue);
            rowUpdateChange.put(column);
        }

        client.updateRow(new UpdateRowRequest(rowUpdateChange));
    }

    public T getRow(Class<T> clazz, Object[] keyColumnValues) {
        try {
            T t = clazz.getDeclaredConstructor().newInstance();
            String[] primaryKeyNames = t.getPrimaryKeyNames();
            String tableName = t.getTableName();

            // 实现从 ots 根据主键和表名称，获取内容;
            PrimaryKey primaryKey = getPrimaryKeyFromObjectArray(primaryKeyNames, keyColumnValues);
            //读取一行数据，设置数据表名称。
            SingleRowQueryCriteria criteria = new SingleRowQueryCriteria(tableName, primaryKey);

            // 如果从 OTS 取到了数据， 设置主键对应列的值
            //设置读取最新版本。
            criteria.setMaxVersions(1);
            GetRowResponse getRowResponse = client.getRow(new GetRowRequest(criteria));
            Row row = getRowResponse.getRow();
            return readRowData(row);
        } catch (Exception e) {
            String msg = "Failed to get row from tablestore for params:" + JSON.toJSONString(keyColumnValues);
            log.error(msg, e);
            throw new RuntimeException(e);
        }

    }

    /**
     * @param clazz
     * @param keyColumnValues 主键列对应的值， 主键列可以是多个列，顺序跟指定的 class 中定义的主键列的顺序一致.
     * @return
     */
    public void deleteRow(Class<T> clazz, Object[] keyColumnValues) {
        try {
            //构造主键:
            T t = clazz.getDeclaredConstructor().newInstance();
            String[] primaryKeyNames = t.getPrimaryKeyNames();
            String tableName = t.getTableName();

            PrimaryKey primaryKey = constructPrimaryKey(primaryKeyNames, keyColumnValues);

            //设置数据表名称。
            RowDeleteChange rowDeleteChange = new RowDeleteChange(tableName, primaryKey);

            client.deleteRow(new DeleteRowRequest(rowDeleteChange));

        } catch (Exception e) {
            //TODO: error logging
            String msg = "Failed to delete row from tablestore for params:" + JSON.toJSONString(keyColumnValues);
            throw new RuntimeException(e);
        }

    }

    private Column buildColumn(String columnName, Object columnValue) {
        ColumnValue cValue = toColumnValue(columnValue);
        return new Column(columnName, cValue);
    }

    private ColumnValue toColumnValue(Object value) {
        ColumnValue cValue;
        if (value instanceof String) {
            cValue = ColumnValue.fromString(String.valueOf(value));
        } else if (value instanceof Long) {
            cValue = ColumnValue.fromLong((Long)value);
        } else if (value instanceof Boolean) {
            cValue = ColumnValue.fromBoolean((Boolean)value);
        } else if (value instanceof Double) {
            Double v = Double.parseDouble(String.valueOf(value));
            cValue = ColumnValue.fromDouble(v);
        } else if (value instanceof byte[]) {
            cValue = ColumnValue.fromBinary((byte[])value);
        } else if (value instanceof JSONArray) {
            cValue = ColumnValue.fromString(value.toString());
        } else if (value instanceof JSONObject) {
            cValue = ColumnValue.fromString(value.toString());
        } else if (value instanceof Integer) {
            Integer v = Integer.parseInt(String.valueOf(value));
            cValue = ColumnValue.fromLong(v.longValue());
        } else {
            String msg = "Type " + value.getClass().getCanonicalName() + " is not supported by Tablestore";
            throw new RuntimeException(msg);
        }
        return cValue;
    }

    /**
     * 从输入的对象，和指定的主键列名称，构建 OTS 主键
     *
     * @param primaryKeyNames 主键名称
     * @param jsonObject      JSON 对象的数据
     * @return
     */
    private PrimaryKey getPrimaryKeyAndRemovePkFromObject(String[] primaryKeyNames, JSONObject jsonObject) {
        //构造主键。
        PrimaryKeyBuilder primaryKeyBuilder = PrimaryKeyBuilder.createPrimaryKeyBuilder();

        for (String primaryKeyName : primaryKeyNames) {
            // 自动检测 PK Column 类型
            ColumnValue columnValue = toColumnValue(jsonObject.get(primaryKeyName));
            primaryKeyBuilder.addPrimaryKeyColumn(primaryKeyName, PrimaryKeyValue.fromColumn(columnValue));

            //从对象中删除 PrimaryKey 的字段，以便保留属性字段，保存到 OTS 的属性列中
            jsonObject.remove(primaryKeyName);
        }

        PrimaryKey primaryKey = primaryKeyBuilder.build();
        return primaryKey;
    }

    /**
     * 获取主键
     * 从object数组中获取
     * 【注意这里的主键顺序与object数组中的主键顺序得一致】
     * 主键 pk+id  object数组中得 对应 pk值+id值
     *
     * @param primaryKeyNames
     * @param keyColumnValues
     * @return
     */
    private PrimaryKey getPrimaryKeyFromObjectArray(String[] primaryKeyNames, Object[] keyColumnValues) {
        //构造主键。
        PrimaryKeyBuilder primaryKeyBuilder = PrimaryKeyBuilder.createPrimaryKeyBuilder();

        int i = 0;
        for (String primaryKeyName : primaryKeyNames) {
            // 自动检测 PK Column 类型
            ColumnValue columnValue = toColumnValue(keyColumnValues[i]);
            primaryKeyBuilder.addPrimaryKeyColumn(primaryKeyName,
                PrimaryKeyValue.fromColumn(columnValue));
            i++;
        }

        PrimaryKey primaryKey = primaryKeyBuilder.build();
        return primaryKey;
    }

    private PrimaryKey constructPrimaryKey(String[] primaryKeyNames, Object[] keyColumnValues) {

        assert primaryKeyNames.length == keyColumnValues.length;

        PrimaryKeyBuilder primaryKeyBuilder = PrimaryKeyBuilder.createPrimaryKeyBuilder();
        for (int i = 0; i < primaryKeyNames.length; i++) {
            // 自动检测 PK Column 类型
            ColumnValue columnValue = toColumnValue(keyColumnValues[i]);
            primaryKeyBuilder.addPrimaryKeyColumn(primaryKeyNames[i], PrimaryKeyValue.fromColumn(columnValue));
        }

        return primaryKeyBuilder.build();
    }
}
```

## 3.Define model class & ModelData class

```Java
public class Employee implements Serializable {
    private String id;

    private String name;

    private Long createdAt;
  
    private Long updatedAt;
}

public class EmployeeData extends Employee implements ColumnData {

    @Override
    public String[] getPrimaryKeyNames() {
        return new String[]{"id"};
    }

    @Override
    public String getTableName() {
        return "t_employee";
    }


    /**
     * 创建索引的时候 添加createdAt 否则不能进行排序查询
     * 索引列：id + name + createdAt
     * @return
     */
    @Override
    public String getDefaultSearchIndexName() {
        return "t_employee_id_name_createdAt";
    }
}

```

Define the extended mapper class based on general DataMapper to implement methods not covered by the default put/get/update/delete.

```Java
@Component
@Slf4j
public class EmployeeMapper extends DataMapper<EmployeeData> {
    //....
}
```

And can use the DataMapper to access tablestore.

```Java
  DataMapper<EmployeeData> mapper = new DataMapper();
  mapper.putRow(employeeData);
```
