Faiss 较老版本的用法 v.1.6.x

From:
https://www.zaxtyson.cn/archives/164/

相关文件
```
faiss/IndexFlat.h
faiss/IndexFlat.cpp
faiss/utils/Heap.h
faiss/utils/Heap.cpp
faiss/utils/utils.h
faiss/utils/ordered_key_value.h
faiss/utils/distances.cpp
faiss/utils/AuxIndexStructures.h
faiss/utils/AuxIndexStructures.cpp
```

源码解析
IndexFlat
IndexFlat 是最简单的索引, 通过暴力搜索找到最近的向量。它不对原始向量数据做处理，而是直接保存向量数据。

搜索时，根据距离算法使用最大/小堆得到 topK 个最近的向量id和距离。

struct IndexFlat: Index {
    // 向量数据库, 存储 add 添加的原始向量数据, 大小 ntotal*d
    std::vector<float> xb;
        
    // 构造函数
    // d 为向量维度, 默认使用 L2 计算距离
    explicit IndexFlat(idx_t d, MetricType metric = METRIC_L2);

    ...
};
add 方法
// 添加向量
void IndexFlat::add (idx_t n, const float *x) {
    xb.insert(xb.end(), x, x + n * d);  // 将数组添加到 xb 尾部
    ntotal += n;
}
注意 IndexFlat 索引没有重写 add_with_ids 方法，这意味着你不能自定义向量的 id

不过，可以配合 IDMap 对向量 id 与自定义 id 之间建立映射关系

建议使用工厂方法创建索引:

```
// 创建一个 768 维， 支持自定义向量id的 Flat 索引， 距离算法为 L2
faiss::Index* index = faiss::index_factory(768, "IDMap,Flat", faiss::MetricType::METRIC_L2);
reset 方法
// 清空存储的向量
void IndexFlat::reset() {
    xb.clear();
    ntotal = 0;
}
```

search 方法

```
// 检索相似向量, 传入 n 个 d 维向量, 返回 n*k 个向量编号和距离
// n 为 query vectos 的数量
// x 为 query vectors 数组
// k 表示需要返回 topK 个向量
// distances 为保存向量距离的数组
// labels 为保存向量编号的数组
void IndexFlat::search(
        idx_t n,
        const float* x,
        idx_t k,
        float* distances,
        idx_t* labels) const {
    // k<=0 会抛异常, faiss::FaissException
    FAISS_THROW_IF_NOT(k > 0);

    if (metric_type == METRIC_INNER_PRODUCT) {
            // float_minheap_array_t 定义于 Heap.h, 最小堆
        // 数据存在 labels distances 两个数组内, 后面使用 reorder 对数据排序
        float_minheap_array_t res = {size_t(n), size_t(k), labels, distances};
        
        // 使用 KNN 求出距离, 距离算法为IP
        // xb 为向量数据库, d 为向量维度, ntotal 为向量数据库中向量的个数
        knn_inner_product(x, xb.data(), d, n, ntotal, &res);
        
    } else if (metric_type == METRIC_L2) {
            // 距离算法为 L2 时, 使用最大堆
        float_maxheap_array_t res = {size_t(n), size_t(k), labels, distances};
        
        // 使用 KNN 求距离, 距离算法为 L2
        knn_L2sqr(x, xb.data(), d, n, ntotal, &res);
    } else {
            // 其它距离算法
        float_maxheap_array_t res = {size_t(n), size_t(k), labels, distances};
        knn_extra_metrics(
                x, xb.data(), d, n, ntotal, metric_type, metric_arg, &res);
    }
}
```

float_minheap_array_t  float_maxheap_array_t 其实是一个类型别名

```
typedef HeapArray<CMin<float, int64_t>> float_minheap_array_t;
typedef HeapArray<CMax<float, int64_t>> float_maxheap_array_t;
```

CMin Cmax 是用于比较用的模板类

```
// C 表示 comparison, 该结构体在构建堆的时候用来对元素排序
// 构建最小堆时使用, topK 问题中, 使用最小堆可以找到 topK 个最大元素
template <typename T_, typename TI_>
struct CMin {
    typedef T_ T;      // T 元素类型, 这里是 float
    typedef TI_ TI;         // TI 元素的 ID 类型, 这里是 int64_t(idx_t)
    typedef CMax<T_, TI_> Crev; // reference to reverse comparison
    
    // 用于比较元素大小
    inline static bool cmp(T a, T b) {
        return a < b;
    }
    
    // 该函数返回 T 类型的最小值
    inline static T neutral() {
        return std::numeric_limits<T>::lowest();
    }
    
    static const bool is_max = false;
        
    // 返回 -∞ <= x 方向上第一个比 x 小的值
    inline static T nextafter(T x) {
        return cmin_nextafter(x);  // 模板特化为 std::nextafterf<float>(x, -HUGE_VALF)
    }
};
// 构建最大堆时使用, 使用最大堆可以得到集合中 topK 个最小值
template <typename T_, typename TI_>
struct CMax {
    typedef T_ T;
    typedef TI_ TI;
    typedef CMin<T_, TI_> Crev;
    
    // 用于元素排序
    inline static bool cmp(T a, T b) {
        return a > b;
    }
    
    // 该函数返回 T 类型的最大值
    inline static T neutral() {
        return std::numeric_limits<T>::max();
    }
    
    static const bool is_max = true;
    
    // 返回 x => +∞ 方向上第一个比 x 大的值
    inline static T nextafter(T x) {
        return cmax_nextafter(x);  // 模板特化为 std::nextafterf<float>(x, HUGE_VALF);
    }
};
// HeapArray 是最大/小堆的模板类
template <typename C>
struct HeapArray {
    typedef typename C::TI TI;   // 元素 ID 类型, int64_t
    typedef typename C::T T;     // 元素类型, float
    
    // float_minheap_array_t res = {size_t(n), size_t(k), labels, distances};
    // 上面的例子使用初始化列表对下面4个参数赋值
    size_t nh;    // 堆的数量(一次检索n个向量, 就创建n个堆, nh表示n个heap)
    size_t k;     // 每个堆的大小(需要返回k个最近向量, 堆大小就是k)
    TI* ids;      // 调用者传给 search, 用来保存向量编号的数组, 即 labels (n*k)
    T* val;       // 调用者传给 search, 用来保存向量距离的数组, 即 distances (n*k)

    // 获取 distances 数组中, 第 key 个 query vector 对应的分量
    T* get_val(size_t key) {
        return val + key * k;
    }

    // 获取 labels 数组中, 第 key 个 query vector 对应的分量
    TI* get_ids(size_t key) {
        return ids + key * k;
    }

    // 初始化所有的 heap
    void heapify();

    // 对堆重排序
    void reorder();
    
    ...

};
```

当 metric_type == METRIC_INNER_PRODUCT 时, 调用 knn_inner_product

```
int distance_compute_blas_threshold = 20;
int distance_compute_blas_query_bs = 4096;
int distance_compute_blas_database_bs = 1024;
int distance_compute_min_k_reservoir = 100;

// x 为 query vectors 数组
// y 为向量数据库数组(xb)
// d 为向量维度
// nx 为 query vectors 的数量
// ny 为向量数据库中向量的数量
// ha 为最小堆对象
void knn_inner_product(
        const float* x,
        const float* y,
        size_t d,
        size_t nx,
        size_t ny,
        float_minheap_array_t* ha) {
    // ha->k 和 nx 一样, 都是 query vectors 的数量, 通常为 1
    if (ha->k < distance_compute_min_k_reservoir) {
            // ha->val, ha->ids 分别是用户传给 search 的 distances, labels 数组
        // res 以最小堆的形式管理这两个数组的空间, 保存搜索结果
        // 因为是内积操作(余弦相似度), 最小堆得到 topK 个最大值, 即最相似的 topK 个向量
        HeapResultHandler<CMin<float, int64_t>> res(
                ha->nh, ha->val, ha->ids, ha->k);
        if (nx < distance_compute_blas_threshold) {
                // query vectors 小于 20 走这个(一般情况走这个分支)
            exhaustive_inner_product_seq(x, y, d, nx, ny, res);
        } else {
            exhaustive_inner_product_blas(x, y, d, nx, ny, res);
        }
    } else {
        ReservoirResultHandler<CMin<float, int64_t>> res(
                ha->nh, ha->val, ha->ids, ha->k);
        if (nx < distance_compute_blas_threshold) {
            exhaustive_inner_product_seq(x, y, d, nx, ny, res);
        } else {
            exhaustive_inner_product_blas(x, y, d, nx, ny, res);
        }
    }
}

// 在向量数据库中找到 query vectors 的最近的 k 个邻居
template <class ResultHandler>
void exhaustive_inner_product_seq(
        const float* x,
        const float* y,
        size_t d,
        size_t nx,
        size_t ny,
        ResultHandler& res) {
    // 根据类型匹配, 模板实例化 SingleResultHandler = HeapResultHandler<CMin<float, int64_t>>::SingleResultHandler
    // SingleResultHandler 对象中持有 HeapResultHandler 对象的引用, 管理了 distances, labels 数组
    using SingleResultHandler = typename ResultHandler::SingleResultHandler;

// 使用 OpenMP 加速计算
#pragma omp parallel
    {
            // 存储搜索结果用
        SingleResultHandler resi(res);
#pragma omp for
                // nx 为 query vectors 的数量, 通常是 1
        for (int64_t i = 0; i < nx; i++) {
            const float* x_i = x + i * d;   // 第 i 个向量对应的 float 数组
            const float* y_j = y;           // 向量数据库 xb 中第 j 个向量对应的 float 数组(初始状态j=0)

            resi.begin(i);  // 准备存储第 i 个搜索结果
                        
            // 遍历向量数据库中的全部向量, 计算向量与 query vector 的内积
            for (size_t j = 0; j < ny; j++) {
                float ip = fvec_inner_product(x_i, y_j, d);  // 计算内积
                
                // 将内积(距离)与向量编号 j 加入 SingleResultHandler 对象 resi
                // add_result 方法使用 CMin/Cmax 的 cmp 对比元素大小, 完成堆排序
                // 最后留下的结果在 distances, labels 数组中, 作为 search 的返回值
                resi.add_result(ip, j);
                
                y_j += d;   // 指向下一个向量对应的数组
            }
            resi.end();
        }
    }
}

//当 metric_type == METRIC_L2 时, 调用 knn_L2sqr

void knn_L2sqr(
        const float* x,
        const float* y,
        size_t d,
        size_t nx,
        size_t ny,
        float_maxheap_array_t* ha,
        const float* y_norm2) {
        // 此时 y_norm2 为 nullptr
    if (ha->k < distance_compute_min_k_reservoir) {
            // 这里使用最大堆管理 distances, labels 数组
        // 是为了得到 topK 个最小值, 因为使用 L2 计算距离, 越小越相似
        HeapResultHandler<CMax<float, int64_t>> res(
                ha->nh, ha->val, ha->ids, ha->k);

        if (nx < distance_compute_blas_threshold) {
                // 通常走这个分支
            exhaustive_L2sqr_seq(x, y, d, nx, ny, res);
        } else {
            exhaustive_L2sqr_blas(x, y, d, nx, ny, res, y_norm2);
        }
    } else {
        ReservoirResultHandler<CMax<float, int64_t>> res(
                ha->nh, ha->val, ha->ids, ha->k);
        if (nx < distance_compute_blas_threshold) {
            exhaustive_L2sqr_seq(x, y, d, nx, ny, res);
        } else {
            exhaustive_L2sqr_blas(x, y, d, nx, ny, res, y_norm2);
        }
    }
}
template <class ResultHandler>
void exhaustive_L2sqr_seq(
        const float* x,
        const float* y,
        size_t d,
        size_t nx,
        size_t ny,
        ResultHandler& res) {
    using SingleResultHandler = typename ResultHandler::SingleResultHandler;

#pragma omp parallel
    {
        SingleResultHandler resi(res);
#pragma omp for
        for (int64_t i = 0; i < nx; i++) {
            const float* x_i = x + i * d;
            const float* y_j = y;
            resi.begin(i);
            for (size_t j = 0; j < ny; j++) {
                float disij = fvec_L2sqr(x_i, y_j, d);  // 这里计算 L2 距离, 其它操作都一样
                resi.add_result(disij, j);
                y_j += d;
            }
            resi.end();
        }
    }
}
```

remove_ids 方法

```
// 删除指定 id 对应的向量
// sel 为 IDSelector 对象
size_t IndexFlat::remove_ids(const IDSelector& sel) {
        // 遍历数据库中全部向量, 删掉 IDSelector 选中的向量
        // 为什么不用 erase 方法: 每次 erase 删除 pos 号元素时, 都需
    // 要把将 pos + 1 到 最后一个元素全部复制到前一个单元, 然后析构
    // 最后一个元素, 如果数据库向量非常巨大, 且需要删除的向量比较多, 
    // 这个代价是比较大的
    // 下面的算法可以使得一次删除多个向量时, 移动内存的次数最少, 效率高
    
    // 在脑子里模拟一下下面的例子(假设向量是1维的)
    //  i
    // [1, 2, 3, 4, 5, 6] | 删掉 3 5
    //  j
    
    idx_t j = 0;
    for (idx_t i = 0; i < ntotal; i++) {
            // 如果这个 id 对应的向量应该删除, 那么, 
        if (sel.is_member(i)) {
            // is_member 为 true 表示这个向量应该被删掉
            // 此时 j 保持不动, 下一轮循环就会出现 i > j
        } else {
            if (i > j) {
                    // 把第 i 个向量移动到第 j 个向量位置, 其它数据不动
                memmove(&xb[d * j], &xb[d * i], sizeof(xb[0]) * d);
            }
            j++;
        }
    }
    
    // 实际移除的向量数量
    // 自定义向量ID时, id与向量可以是一对多的关系, 删一个id可能同时删掉多个向量
    size_t nremove = ntotal - j;
    if (nremove > 0) {
        ntotal = j;
        xb.resize(ntotal * d);  // 收缩 xb 空间
    }
    return nremove;
}

// 那么, IDSelector 是个什么东西? 它是一个抽象基类, 最重要的是 is_member 方法, 用于判断给定的 id 是否选中(是否需要删除)

struct IDSelector {
    typedef Index::idx_t idx_t;
    virtual bool is_member(idx_t id) const = 0;
    virtual ~IDSelector() {}
};

//它有几个派生类: IDSelectorRange 用于选中一个左闭右开的id区间; IDSelectorArray 用于选中一个id列表; IDSelectorBatch 也是选中一个id列表, 不过内部使用了bloom过滤器和unordered_set 加快判断速度

struct IDSelectorRange : IDSelector {
    idx_t imin, imax;

    IDSelectorRange(idx_t imin, idx_t imax);
    bool is_member(idx_t id) const override;
    ~IDSelectorRange() override {}
};

bool IDSelectorRange::is_member(idx_t id) const {
    return id >= imin && id < imax;   // 很简单的判断一下范围
}

struct IDSelectorArray : IDSelector {
    size_t n;
    const idx_t* ids;

    IDSelectorArray(size_t n, const idx_t* ids);
    bool is_member(idx_t id) const override;
    ~IDSelectorArray() override {}
};

bool IDSelectorArray::is_member(idx_t id) const {
        // 遍历 id 数组, 看看是不是需要删除
    // 如果向量数据库存在 N 个向量, 要删除的 id 数组有 M 个元素
    // 删除操作的时间复杂度为 O(M*N)
    for (idx_t i = 0; i < n; i++) {   
        if (ids[i] == id)
            return true;
    }
    return false;
}
```

通常, 我们使用 IDSelectorBatch 作为 IDSelector, 用于删除向量

```
std::vector<idx_t> to_remove = {10086, 10087, ...};
faiss::IDSelectorBatch selector(to_remove.size(), to_remove.data());
nremove = index->remove_ids(selector);
```

IDSelectorBatch 内部使用了 bloom 过滤器, bloom 过滤器是一种概率型数据结构, 可以快速判断 id 不在集合内(不用删除)的情况

但是它不能准确判断id在集合内的情况(有一定的概率误判), 所以对于某个id是否在集合内, IDSelectorBatch使用 unordered_set (HashSet)确定

```
struct IDSelectorBatch : IDSelector {
    std::unordered_set<idx_t> set;   // 存储需要删除的 id

    typedef unsigned char uint8_t;
    std::vector<uint8_t> bloom; // assumes low bits of id are a good hash value
    int nbits;
    idx_t mask;

    IDSelectorBatch(size_t n, const idx_t* indices);
    bool is_member(idx_t id) const override;
    ~IDSelectorBatch() override {}
};
IDSelectorBatch::IDSelectorBatch(size_t n, const idx_t* indices) {
    nbits = 0;  // 过滤器的 bit 数组长度
    while (n > (1L << nbits))
        nbits++;
    nbits += 5;
    // for n = 1M, nbits = 25 is optimal, see P56659518

    mask = (1L << nbits) - 1;
    bloom.resize(1UL << (nbits - 3), 0);
    for (long i = 0; i < n; i++) {
        Index::idx_t id = indices[i];
        set.insert(id);     // 将 id 加入无序set
        id &= mask;
        bloom[id >> 3] |= 1 << (id & 7);
    }
}
bool IDSelectorBatch::is_member(idx_t i) const {
    long im = i & mask;
    if (!(bloom[im >> 3] & (1 << (im & 7)))) {
        return 0;  // 快速检测 id 不在集合内的情况
    }
    return set.count(i); // bloom 过滤器无法判断才用无序集合判断
}
```

IndexFlatIP
其实就是默认距离算法为 IP 的 IndexFlat 罢了

struct IndexFlatIP : IndexFlat {
    explicit IndexFlatIP(idx_t d) : IndexFlat(d, METRIC_INNER_PRODUCT) {}
    IndexFlatIP() {}
};

IndexFlatL2
这个也一样, 默认距离算法 L2 (其实IndexFlat默认也是L2)

struct IndexFlatL2 : IndexFlat {
    explicit IndexFlatL2(idx_t d) : IndexFlat(d, METRIC_L2) {}
    IndexFlatL2() {}
};

IndexFlat1D
1D表示1维向量, 这个类对 1 维向量的存储和搜索做了优化

不过我们使用的向量通常是高维的, 这里就不关注它的实现细节了

struct IndexFlat1D : IndexFlatL2 {
    bool continuous_update; ///< is the permutation updated continuously?

    std::vector<idx_t> perm; ///< sorted database indices

    explicit IndexFlat1D(bool continuous_update = true);

    /// if not continuous_update, call this between the last add and
    /// the first search
    void update_permutation();

    void add(idx_t n, const float* x) override;

    void reset() override;

    /// Warn: the distances returned are L1 not L2
    void search(
            idx_t n,
            const float* x,
            idx_t k,
            float* distances,
            idx_t* labels) const override;
};
