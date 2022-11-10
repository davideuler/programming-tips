
## 1.Create in memory index

```
    int dim = 128;
    int nlist = 4096;
    faiss::IndexFlat * ann_quantizer = new faiss::IndexFlat(dim, faiss::METRIC_L2);
    faiss::IndexIVFFlat * ann_index = new faiss::IndexIVFFlat(ann_quantizer, dim, nlist, faiss::METRIC_L2);
    ann_index->own_fields = true;
```

## 2.Load IVFFlatIndex from file 

```
faiss::Index * load_IVFFlat_index(const char* index_file_path){
    faiss::Index * index = faiss::read_index(index_file_path, 0);
    return index;
}
```

## 3.Search against the index with IDSelectorBatch to filter some ids

```
#include <random>
#include <vector>

#include <faiss/IndexFlat.h>
#include <faiss/IndexIVFFlat.h>
#include <faiss/impl/AuxIndexStructures.h>
#include <faiss/IVFlib.h>

#include <faiss/index_io.h>
#include <faiss/Index.h>

std::mt19937 rng;

int main(int argc, char** argv) {
    faiss::Index *index = load_IVFFlat_index(index_file);

    faiss::IDSelector::idx_t * filterIds = new faiss::IDSelector::idx_t[4]; // ids to remove
    filterIds[0] = 1234;
    filterIds[1] = 1235;
    filterIds[2] = 1236;
    filterIds[3] = 1237;
    faiss::IDSelectorBatch selector(4, filterIds);

    int nq = 1, dim=128;
    std::vector<float> xq = make_data(nq, dim);

    faiss::IVFSearchParameters params;
    params.max_codes = 0;
    params.nprobe = 16;
    params.sel = &selector;

    int k = 10;
    std::vector<faiss::IDSelector::idx_t> I(k * nq);
    std::vector<float> D(k * nq);
    faiss::ivflib::search_with_parameters(index, nq, xq.data(), k, D.data(), I.data(), &params);

    std::cout << std::endl;
    for (int i = 0; i < I.size(); ++i){
        faiss::IDSelector::idx_t docId = I.at(i);
        std::cout << docId << ":" << D.at(i) << "," << std::endl;
    }
}
```
