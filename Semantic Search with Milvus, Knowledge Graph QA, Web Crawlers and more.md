# Semantic Search with Milvus, Knowledge Graph QA, Web Crawlers and more!

## Build a fully featured pipeline using the latest features from Haystack v0.8.0

Those of you who follow our GitHub repository will know that there has been a lot of activity on [Haystack](https://github.com/deepset-ai/haystack) recently! Not only have we been working hard on a set of new features, but we’ve received a lot of great code contributions and had a lot of interesting and productive conversations with our community. The sum of all this interaction is [our latest release v0.8.0](https://github.com/deepset-ai/haystack/releases/tag/v0.8.0), which features more changes than we could list here. Nonetheless, we wanted to walk you through the most exciting new features that will help you build your own semantic search pipeline.

# Milvus

Everything as a vector. That’s the future that we see for neural search. It’s already working remarkably well in image, natural language and sound, and research is constantly driving us closer to building a single embedding space for all modalities.

With this vision comes the need for vector optimized databases that can perform indexing and similarity calculations fast and so we are very excited to be introducing the [MilvusDocumentStore](https://github.com/deepset-ai/haystack/blob/master/haystack/document_store/milvus.py) in Haystack. Milvus encapsulates multiple Approximate Nearest Neighbours (ANN) libraries such as FAISS and ANNOY but is also built with the robustness and reliability required in production systems. It allows for dynamic data management, it can also run as a separate service via Docker and we found their library very smooth to work with. And of course, they are open source!

A MilvusDocumentStore is the perfect complement to a DPRRetriever or an EmbeddingRetriever and in our experimental runs, we have already seen great performance from it. You can expect to see a blog from us soon with benchmarks of all our retrievers and document stores.

Thanks go to our Github contributor lalitpagaria who was the driving force behind [this new feature](https://github.com/deepset-ai/haystack/pull/771)!

# Knowledge Graph QA

Our ambition with [Haystack](https://www.deepset.ai/haystack) is to build the most comprehensive and practical framework for anything in the field of search or information retrieval and as such, we could not ignore Knowledge Graphs. Many companies build large, well maintained knowledge graphs to accurately capture the interrelations between different concepts and entities in their domain. Following strong interest from our community, we challenged ourselves to build a system that could interpret natural language questions and fetch structured data from such a graph.

![img](https://miro.medium.com/max/1400/0*9yXxJcbus6nV8Xu1)

From [Yashu Seth](https://yashuseth.blog/2019/10/08/introduction-question-answering-knowledge-graphs-kgqa/)

In the latest release, you will see the first small steps we’ve made in this direction. Haystack now has a [GraphDBKnowledgeGraph](https://github.com/deepset-ai/haystack/blob/master/haystack/knowledge_graph/graphdb.py) class which stores your triples and executes SPARQL queries. There is also a [Text2SparqlRetriever](https://github.com/deepset-ai/haystack/blob/master/haystack/graph_retriever/text_to_sparql.py) class which connects to a GraphDBKnowledgeGraph and functions as a semantic parser. It turns natural language questions into SPARQL queries using a BART sequence-to-sequence model. Thanks must go to the [Transformers](https://github.com/huggingface/transformers) library maintained by Huggingface which has made it incredibly easy to integrate new transformers models into Haystack!

Knowledge graph QA systems have a key advantage over extractive QA systems in that they can handle questions that require counting or operations like taking the maximum or minimum. However, the extraction of relational triples and the training of the semantic parser is by no means straightforward. But when done right, we see a lot of potential in the ensembling of the two methods.

If you want to see how to work with Knowledge Graphs in Haystack, please check out [our end-to-end tutorial](https://github.com/deepset-ai/haystack/blob/master/tutorials/Tutorial10_Knowledge_Graph.ipynb)! This will give you a sense of the first small successes we’ve had with the technique and we would love to hear from you if you want to drive Knowledge Graph QA forward with us!

# **Pipeline Configs**

The flexibility of Pipelines in Haystack has proven to be very popular with our community and we ourselves have enjoyed experimenting with different configurations. For example, we created Pipelines where a BM25 retriever is ensembled with a DPR retriever to get the best of both worlds and it is now possible in Haystack to build retrieval systems that return not only the full document text, but also their summaries and translations.

Now, with the introduction of Pipeline config files, it is easier than ever to define, save and load your custom Pipeline. Rather than writing lines of code to tweak Pipelines, everything that configures a Pipeline can be written in a YAML file allowing for easier and quicker experimentation cycles and also simpler maintenance of production systems.

This is an example of what a YAML config might look like.

![img](https://miro.medium.com/max/1400/0*3JVJdCz-rRZXwp8w)

These few lines are all you need to load that config and run a Pipeline.

![img](https://miro.medium.com/max/1400/0*rmSWpVh18Mi3naUF)

These configs are here to lower the barriers to entry, and allow you to get creative with your Pipeline designs.

# Confidence Scores

Apart from seeing your model’s top predictions, it is often very helpful to know how confident the model is in its predictions. For example, you might be building a system where you expect 90% accuracy and would rather route a request elsewhere if the model is unsure. The Softmaxed scores coming from a Question Answering head do not necessarily capture the model’s confidence of an answer being correct and can create many problems in practice.

The latest release takes us a step in the right direction as each prediction is now accompanied by a `probability` score in the range of 0 to 1, with values near 0 meaning very low confidence in the prediction and values near 1 meaning very high confidence. Using our transfer learning framework FARM, you can even go one step further and tune this `probability` score to be aligned with your metrics so that you can take confidence=0.9 to mean that the model will be right 90% of the time. If this is something that you’re interested in, have a look at [this tutorial](https://github.com/deepset-ai/FARM/blob/master/examples/question_answering_confidence.py).

There are many different approaches and complexities to calculating model confidence but you can expect further support and new tools to help you in tuning your system.

# Web Crawler

Finally, it is central to Haystack’s design that it connects easily to other components and data sources. For this reason, we want to highlight a very nice community contribution from DIVYA-19 that has added a [web crawler](https://github.com/deepset-ai/haystack/pull/775) to Haystack! Simply provide URLs of pages you’d like to search over and have the Crawler convert them into Haystack documents.

We anticipate that more use cases will pop up where there is a need to connect data from different sources, formats and streams. If you are working with a certain application, data source or platform that is missing a connection to Haystack, please feel free to bring this to our attention in our GitHub repository or [through Slack](https://haystack.deepset.ai/community/join)! Haystack is designed to be an end-to-end search system but it is also our goal to make sure it integrates seamlessly into your tech stack.

# Conclusion

This latest release is packed full of new features and improvements, so much so that we didn’t even find space in this blog to talk about Evaluation Nodes or SQuAD to DPR data scripts. Haystack v0.8.0 is available now and you can see a full list of changes in [our release notes](https://github.com/deepset-ai/haystack/releases/tag/v0.8.0).
