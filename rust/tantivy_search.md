
### 1.Merge all segments of an Index

https://github.com/quickwit-oss/tantivy/issues/1618

``` rust
    // for newly created index, wait merging threads for later merging of all segments
    // index_writer.wait_merging_threads()?; 
    let segment_ids = index.searchable_segment_ids()?;
    let mut index_writer = index
        .writer(1_500_000_000)
        .expect("failed to create index writer");
    block_on(index_writer.merge(&segment_ids))?;
    block_on(index_writer.garbage_collect_files())?;
```

### 2.Retrieve field value in FastField

Declare a fast field:

```rust
    let mut schema_builder = Schema::builder();

    // set the _docId to be INDEXED for query & delete
    schema_builder.add_i64_field("_docId", NumericOptions::default() | STORED | INDEXED | FAST);
```

Can query value from a fast field of Long like this:
```rust
       let segment_reader = index_searcher.segment_reader(segment_id);
       let doc_id_reader = segment_reader.fast_fields().i64(doc_id_field).unwrap();
       let doc_id = doc_id_reader.get_val(doc_address.doc_id);
```

The following example execute a query, and get all _docIds from the fastfield.

```rust
    let doc_id_field = searcher.schema.get_field("_docId").unwrap();
    let collector = DocSetCollector{};
    let doc_addresses = index_searcher.search(&query, &collector)?;
    
    let mut seg_id_readers :HashMap<u32, std::sync::Arc<dyn Column<i64>>> = HashMap::new();

    for doc_address in doc_addresses {
        // cache doc_id_reader by segment_ord,
        let segment_id = doc_address.segment_ord.clone();

        let doc_id_reader_option = seg_id_readers.get(&segment_id);
        match doc_id_reader_option {
            Some(doc_id_reader) => {
                let doc_id = doc_id_reader.get_val(doc_address.doc_id);
                //processing docId
            }
            None => {
                let segment_reader = index_searcher.segment_reader(segment_id);
                let doc_id_reader = segment_reader.fast_fields().i64(doc_id_field).unwrap();
                let doc_id = doc_id_reader.get_val(doc_address.doc_id);
                seg_id_readers.insert(segment_id, doc_id_reader);
                //processing docId
            }
        }
        
    }
```

### 3.FastField Collector for all values of the matched field

```rust
// Fast field (i64/u64) value collector, the i64/u64 value(like a docId) is collected into a RoaringBitmap

use std::sync::Arc;
use std::time::Instant;
use futures::executor::block_on;

use roaring::RoaringTreemap;

use tantivy::collector::{Collector, SegmentCollector};
use tantivy::directory::MmapDirectory;
use tantivy::fastfield::Column;
use tantivy::query::TermQuery;
use tantivy::schema::{Schema, FAST, INDEXED, TEXT, IndexRecordOption};
use tantivy::{doc, Index, Score, SegmentReader, Term};

#[derive(Default)]
struct Stats {
    bitmap: RoaringTreemap,
}

impl Stats {
    fn stat_self(self) -> Option<Stats> {
        Some(self)
    }
}

struct FastFieldCollector {
    field: String,
}

impl FastFieldCollector {
    fn with_field(field: String) -> FastFieldCollector {
        FastFieldCollector { field: field}
    }
}

impl Collector for FastFieldCollector {
    // That's the type of our result.
    // Our standard deviation will be a float.
    type Fruit = Option<Stats>;

    type Child = FastFieldSegmentCollector;

    fn for_segment(
        &self,
        _segment_local_id: u32,
        segment_reader: &SegmentReader,
    ) -> tantivy::Result<FastFieldSegmentCollector> {
        let fast_field_reader = segment_reader.fast_fields().i64(self.field.as_str())?;
        
        Ok(FastFieldSegmentCollector {
            fast_field_reader,
            stats: Stats::default(),
        })
    }

    fn requires_scoring(&self) -> bool {
        // this collector does not care about score.
        false
    }

    fn merge_fruits(&self, segment_stats: Vec<Option<Stats>>) -> tantivy::Result<Option<Stats>> {
        let mut stats = Stats::default();
        for segment_stats in segment_stats.into_iter().flatten() {
            stats.bitmap  = stats.bitmap | segment_stats.bitmap;
        }
        Ok(stats.stat_self())
    }
}

struct FastFieldSegmentCollector {
    fast_field_reader: Arc<dyn Column<i64>>,
    stats: Stats,
}

impl SegmentCollector for FastFieldSegmentCollector {
    type Fruit = Option<Stats>;

    fn collect(&mut self, doc: u32, _score: Score) {
        let value = self.fast_field_reader.get_val(doc) as i64;
        self.stats.bitmap.insert(value.unsigned_abs());
    }

    fn harvest(self) -> <Self as SegmentCollector>::Fruit {
        self.stats.stat_self()
    }
}
```

