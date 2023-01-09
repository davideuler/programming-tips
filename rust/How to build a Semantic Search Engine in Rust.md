# How to build a Semantic Search Engine in Rust

![img](https://miro.medium.com/max/1400/1*CpY8K_hAPXQ8jKM1KNGmMw.png)

From:
* https://sachaarbonel.medium.com/how-to-build-a-semantic-search-engine-in-rust-e96e6378cfd9
* https://github.com/sachaarbonel/semantic-search

“A Crab Searching for books in a book shelf using a magnifying glass”

# Introduction

A [semantic search](https://en.wikipedia.org/wiki/Semantic_search) engine is a type of [recommender system](https://en.wikipedia.org/wiki/Recommender_system) that relies on the meaning of words to provide better search results. It is different from a traditional full text search engine, which relies on keyword matching to provide results.

A semantic search engine allows you to search for concepts, not just keywords. It understands meaning and the relationships between different concepts and can provide more relevant results based on those relationships.

In this article, we will discuss how to build a semantic search engine in [Rust](https://www.rust-lang.org/). We’ll explain what are embeddings, transformers, and nearest neighbor searches and how to perform them using KD-trees.

# What Are Embeddings?

[Embedding](https://en.wikipedia.org/wiki/Embedding) is a term used in machine learning and statistics. Embeddings are mathematical representations of data that can be used for dimensionality reduction, similarity measurement, and many other tasks.

In [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing) (NLP), text embedding is a mapping of a word or phrase into a vector of real numbers. The vector represents the word or phrase in a high-dimensional space.

The idea of word embeddings was first proposed in the early 2000s, but it wasn’t until 2013 that they became widely used with the release of the [word2vec](https://en.wikipedia.org/wiki/Word2vec) algorithm and then [BERT](https://en.wikipedia.org/wiki/BERT_(language_model)) in 2018.

# What Is a Transformer?

Embeddings are used in NLP tasks such as machine translation, question answering, and text classification. They are also used in recommender systems and [knowledge graphs](https://en.wikipedia.org/wiki/Knowledge_graph).

A [transformer](https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)) is a type of neural network that can be used for NLP tasks such as machine translation and question answering. The transformer was first proposed in 2017 in the paper Attention Is All You Need.

Transformers are different from traditional recurrent neural networks (RNNs) in that they do not require sequential data. This makes them well suited for tasks like machine translation, where the input and output are not necessarily in the same order.

Transformers are also more parallelizable than RNNs, which makes them faster to train.

Sentence Transformers is a state-of-the-art model for text and image embeddings.

# How to Use Sentence Transformers for Text Embeddings?

The [rust-bert](https://crates.io/crates/rust-bert) crate provides ready-to-use NLP pipelines and transformer-based models (BERT, DistilBERT, GPT2,…) in Rust. The crate also provides a Sentence Embeddings model.

In this article, we will use the rust-bert library to generate text embeddings. We will use the [all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2) model, which is a pre-trained model that uses the MiniLM [architecture](https://arxiv.org/abs/2002.10957).

For example, to get the text embedding for the sentence “this is an example sentence” and “each sentence is converted”:

```
let model = SentenceEmbeddingsBuilder::remote(SentenceEmbeddingsModelType::AllMiniLmL12V2).create_model()?;

let sentences = [
    "this is an example sentence", 
    "each sentence is converted"
];
    
let output = model.predict(&sentences);
```


# Nearest Neighbor Search

A [nearest neighbor search](https://en.wikipedia.org/wiki/Nearest_neighbor_search) is a method for finding the closest datapoint to a given query point. The query point can be any datapoint, not just a point in the dataset.

The goal of a nearest neighbor search is to find the datapoint that is most similar to the query point. Similarity can be measured using any distance metric, such as the Euclidean distance or the cosine similarity.

# What Is a KD-Tree?

A [KD-tree](https://en.wikipedia.org/wiki/K-d_tree) is a type of data structure that can be used for efficient nearest neighbor searches. A KD-tree is a [binary tree](https://en.wikipedia.org/wiki/Binary_tree) where each node is divided into two children based on a splitting criterion.

The splitting criterion can be any function that maps a datapoint to a real number. The most common splitting criterion is the Euclidean distance.

KD-trees are very efficient for nearest neighbor searches because they reduce the search space by half at each level of the tree.

For example, if we want to find the datapoint that is nearest to the point (3.1, 0.9, 2.1), we can use a KD-tree to reduce the search space from the entire dataset to just the datapoints that are closest to (3.1, 0.9, 2.1).

In Rust, we can use the [kd-tree](https://crates.io/crates/kd-tree) crate to build a KD-tree. We can use the build_by_ordered_float function to create a KD-tree from a list of points.

```
let kdtree = kd_tree::KdTree::build_by_ordered_float(vec![
    [1.0, 2.0, 3.0],
    [3.0, 1.0, 2.0],
    [2.0, 3.0, 1.0],
]);

// search the nearest neighbor
let found = kdtree.nearest(&[3.1, 0.9, 2.1]).unwrap();
```

# Implementing a Semantic Search Engine

In this section, we will discuss how to build a semantic search engine in Rust. We will use the Rust NLP crates rust-bert and kd-tree to perform similarity searches on books. In applications, it is a feature usually referred to as “Similar Books”.

Now we can write the code for our semantic search engine. We will start by loading our data stored in json, encode the embeddings and feed them to our kdtree.

## Prerequisites

Having Rust installed

## Depedencies

Let’s create our project called “semantic-search”

```
cargo new semantic-search
```

And add our dependencies we need

```
cd semantic-search 
cargo add serde --features derive 
cargo add rust-bert 
cargo add anyhow 
cargo add kd-tree 
cargo add typenum
```

## Representing Our Books in Json

Create a file called `books.json` to store our json data.

```
{
    "books": [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "summary": "The story primarily concerns the young and mysterious millionaire Jay Gatsby and his quixotic passion and obsession with the beautiful former debutante Daisy Buchanan."
        },
        {
            "title": "The Catcher in the Rye",
            "author": "J. D. Salinger",
            "summary": "The story is told in the first person by Holden Caulfield, a cynical teenager who recently has been expelled from prep school."
        },
        {
            "title": "The Grapes of Wrath",
            "author": "John Steinbeck",
            "summary": "The novel tells the story of the Joad family, who are driven from their Oklahoma homestead and forced to travel west to the promised land of California."
        }
    ]
}

```

## Deserializing Our Json Data Into A Struct

Our program will load the json data into a struct. We can use the serde crate to deserialize the json data into our struct.

```
use serde::{Deserialize};

#[derive(Debug, Deserialize)]
pub struct Library {
    pub books: Vec<Book>,
}

#[derive(Debug, Deserialize, Clone)]
pub struct Book {
    pub title: String,

    pub author: String,

    pub summary: String,
}
```

We can now read the json from a file using the std::fs module and deserialize the json into our Book struct.

```
fn main() -> anyhow::Result<()> {

let json = fs::read_to_string("data/books.json")?;
let library: Library = serde_json::from_str(&json)?;
for book in library.books.clone() {
    println!("Embedding book: {}", book.title);
}

    Ok(())
}
```

## Encoding Book Summaries Into Embeddings

We can now use our model to encode each of our book summaries into embeddings. We will use the `rust-bert` crate to perform the encoding. We'll also need a convenient method to convert our book model into an Embedded book model.

```
#[derive(Debug)]
pub struct EmbeddedBook {
    pub title: String,

    pub author: String,

    pub summary: String,

    pub embeddings: [f32; 384],
}

impl Book {
    fn to_embedded(self, embeddings: [f32; 384]) -> EmbeddedBook {
        EmbeddedBook {
            title: self.title,
            author: self.author,
            summary: self.summary,
            embeddings: embeddings,
        }
    }
}

// convenient to convert a slice to a fixed size array
fn to_array(barry: &[f32]) -> [f32; 384] {
    barry.try_into().expect("slice with incorrect length")
}
```

Finally, call encode for each book and add it to the embeddedbooks vector:

```
fn main() -> anyhow::Result<()> {

+ let model = SentenceEmbeddingsBuilder::remote(SentenceEmbeddingsModelType::AllMiniLmL12V2).create_model()?;
let json = fs::read_to_string("data/books.json")?;
let library: Library = serde_json::from_str(&json)?;
+ let mut embeddedbooks = Vec::new();
for book in library.books.clone() {
-    println!("Embedding book: {}", book.title);
+    let embeddings = model.encode(&[book.clone().summary])?;
+    let embedding = to_array(embeddings[0].as_slice());
+    embeddedbooks.push(book.to_embedded(embedding));
}

    Ok(())
}
```

## Creating the KD-tree

Before performing our search, first, we need to create a KD-tree from our embeddedbooks vector. We can do this using the sort_by function from the kd-tree crate.

We also need to implement the KdPoint trait for our EmbeddedBook struct. This trait allows us to use our EmbeddedBook struct with the kd-tree crate.

```
impl KdPoint for EmbeddedBook {
    type Scalar = f32;
    type Dim = typenum::U2; // 2 dimensional tree.
    fn at(&self, k: usize) -> f32 {
        self.embeddings[k]
    }
}
```

Now we can use the sort_by function to create a KD-tree from our embeddedbooks vector.

```
fn main() -> anyhow::Result<()> {

let model = SentenceEmbeddingsBuilder::remote(SentenceEmbeddingsModelType::AllMiniLmL12V2).create_model()?;
let json = fs::read_to_string("data/books.json")?;
let library: Library = serde_json::from_str(&json)?;
 let mut embeddedbooks = Vec::new();
for book in library.books.clone() {
    println!("Embedding book: {}", book.title);
    let embeddings = model.encode(&[book.clone().summary])?;
    let embedding = to_array(embeddings[0].as_slice());
    embeddedbooks.push(book.to_embedded(embedding));
}
+  let kdtree = kd_tree::KdSlice::sort_by(&mut embeddedbooks, |item1, item2, k| {
+        item1.embeddings[k]
+            .partial_cmp(&item2.embeddings[k])
+            .unwrap()
+    });

Ok(())
}
```

## Performing the Nearest Neighbour Search

Now that we have encoded our books into embeddings, we can use a nearest neighbor search to find the book that is most similar to a given query.

We need a convenient topic method on EmbeddedBook to create a dummy book with authors, title etc to for topic embedding.

```
impl EmbeddedBook {
    fn topic(embeddings: [f32; 384]) -> Self {
        Self {
            title: None,
            author: None,
            summary: None,
            embeddings: embeddings,
        }
    }
}
```

We can use the kd-tree crate’s nearests function to perform the search. This function takes a query point and a number of results to return.

In this case, we will use the query “rich” and return 10 results.

```
fn main() -> anyhow::Result<()> {

let model = SentenceEmbeddingsBuilder::remote(SentenceEmbeddingsModelType::AllMiniLmL12V2).create_model()?;
let json = fs::read_to_string("data/books.json")?;
let library: Library = serde_json::from_str(&json)?;
 let mut embeddedbooks = Vec::new();
for book in library.books.clone() {
    println!("Embedding book: {}", book.title);
    let embeddings = model.encode(&[book.clone().summary])?;
    let embedding = to_array(embeddings[0].as_slice());
    embeddedbooks.push(book.to_embedded(embedding));
}
let kdtree = kd_tree::KdSlice::sort_by(&mut embeddedbooks, |item1, item2, k| {
    item1.embeddings[k]
    .partial_cmp(&item2.embeddings[k]).unwrap()
});
+ let query = "rich";
+ println!("Querying: {}", query);
+ let rich_embeddings = model.encode(&[query])?;
+ let rich_embedding = to_array(rich_embeddings[0].as_slice());
+ let rich_topic = EmbeddedBook::topic(rich_embedding);
+ let nearests = kdtree.nearests(&rich_topic, 10);
+ for nearest in nearests {
+     println!("nearest: {:?}", nearest.item.title);
+     println!("distance: {:?}", nearest.squared_distance);
+}
Ok(())
}
```

After running our program, this is what we are getting

![img](https://miro.medium.com/max/1400/0*jLUVQSU46QfnPU9o)

# Conclusion

In this article, we’ve discussed how to build a basic semantic search engine in Rust. We’ve explained what are embeddings, transformers, and nearest neighbor searches, and how to perform them using KD-trees.

We’ve also discussed how to use the rust-bert crate to generate text embeddings, and how to use the kd-tree crate to perform nearest neighbor searches.

You can find the source code in this [repository](https://github.com/sachaarbonel/semantic-search).

**Where to go from here? What can we improve?**

Well, keeping those embeddings in memory and running the model everytime we run the program is not a very scalable solution, in a real world scenario. Also this kd-tree crate doesn’t support removing or updating nodes in our tree. You could try this [rs-annoy](https://github.com/uzushino/rs-annoy) project. Annoy is what is used at Spotify to store embeddings of songs. There is also this [hora](https://github.com/hora-search/hora) completely written in Rust.

You could serialize the embedded books using the [bincode](https://crates.io/crates/bincode) crate on the EmbeddedBook struct along with the [serde-big-array](https://crates.io/crates/serde-big-array) create for the serialization on our embedding field. There is an example on how to do serialize structs into binary in [this Rust by example guide](https://rust-by-example-ext.com/serde/bincode.html), the struct just have to derive the Serialize trait from serde.

Or you could use the [pgvector Postgres extension](https://github.com/pgvector/pgvector) and the [corresponding Rust crate](https://crates.io/crates/pgvector) to respectively store them on postgres and query them using their builtin operator `<->` for performing neighbour search.

Instead of our cli, we can also serve our recommendations to end users by wrapping our engine using a REST api with [axum](https://crates.io/crates/axum) for example.
