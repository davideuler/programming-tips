
### Merge all segments of an Index

``` rust
    let segment_ids = index.searchable_segment_ids()?;
    let mut index_writer = index
        .writer(1_500_000_000)
        .expect("failed to create index writer");
    block_on(index_writer.merge(&segment_ids))?;
    block_on(index_writer.garbage_collect_files())?;
```

### Retrieve field value in FastField

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
