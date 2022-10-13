## Project reference for rocksdb abstraction

### RocksDB In Kafka
https://github.com/apache/kafka/blob/322a065b9055649c713baf43f154052d45cd1588/streams/src/main/java/org/apache/kafka/streams/state/internals/RocksDBStore.java
https://github.com/apache/kafka/blob/acd1f9c5631ed2aec2d6ab238e6b81c1a9eb47a2/streams/src/test/java/org/apache/kafka/streams/state/internals/RocksDBStoreTest.java

https://github.com/a0x8o/kafka/blob/master/streams/src/main/java/org/apache/kafka/streams/state/internals/RocksDbIterator.java

### Column Family in RocksDB
https://github.com/facebook/rocksdb/wiki/Column-Families
https://github.com/facebook/rocksdb/blob/main/examples/column_families_example.cc

Column family can be processed as a table in database. each Column Family has different <Key, Value> types mapping with a column family name as identifier.

### RocksDB Table abstraction in Hadoop ozone

Ozone is a distributed object store for Hadoop based on Raft(Apache Ratis) and RockDB. Ozone can be run on Kubernetes.
Ozone comes with a Java client library, S3 protocol support, and a command line interface which makes it easy to use Ozone.

Table: 
https://github.com/apache/ozone/blob/3d3e9eaf00/hadoop-hdds/framework/src/main/java/org/apache/hadoop/hdds/utils/db/Table.java

RDBStore:
https://github.com/apache/ozone/blob/3d3e9eaf00/hadoop-hdds/framework/src/main/java/org/apache/hadoop/hdds/utils/db/RDBStore.java
https://github.com/apache/ozone/blob/3d3e9eaf00/hadoop-hdds/framework/src/main/java/org/apache/hadoop/hdds/utils/db/RDBTable.java

RDBStore & createTable()
https://www.programcreek.com/java-api-examples/?code=apache%2Fhadoop-ozone%2Fhadoop-ozone-master%2Fhadoop-hdds%2Fframework%2Fsrc%2Fmain%2Fjava%2Forg%2Fapache%2Fhadoop%2Fhdds%2Futils%2FRocksDBStore.java#

```
public void createTable(String name, ColumnFamilyOptions options) throws IOException {
    if (handleTable.containsKey(name)) {
      return;
    }
    ColumnFamilyDescriptor columnFamilyDescriptor = new ColumnFamilyDescriptor(
            StringUtils.string2Bytes(name),
            options
    );
    ColumnFamilyHandle handle;
    try {
      handle = db.createColumnFamily(columnFamilyDescriptor);
    } catch (RocksDBException e) {
      throw new RuntimeException("Failed to create ColumnFamily, name:" + name, e);
    }
    handleTable.put(name, handle);
  }
```

For options:
https://github.com/facebook/rocksdb/wiki/Basic-Operations
https://github.com/facebook/rocksdb/wiki/Setup-Options-and-Basic-Tuning

https://www.programcreek.com/java-api-examples/?class=org.rocksdb.RocksIterator&method=close

Loop through all record in a table with id > lastDocumentId (to performan a range scan, alse can set the upper bound ):

```
            Table<Long, Document> table = rdbStore.getTable(tableName, Long.class, Document.class);
            TableIterator<Long, ? extends KeyValue<Long, Document>> iterator = table.iterator();

            iterator.seek(lastDocumentId);
            while (iterator.hasNext()) {
                KeyValue<Long, Document> element = iterator.next();
                Document document = element.getValue();
                //....
            }
```


## Ozone Architecture:
https://ozone.apache.org/docs/1.2.1/concept/overview.html
https://ozone.apache.org/docs/1.2.1/concept/storagecontainermanager.html
