
## 中文分词，完全禁用结巴词库，禁用新词识别

```
  import jieba

  jieba.set_dictionary("words.txt")

  seg_list = jieba.cut("helloworldfromhangzhou你好世界", HMM=False)
  print(", ".join(seg_list))
```

## 计算两个中文句子的相似度 - Option 1

```
  ## text2vec 依赖于 pytorch, 重量级的相似度计算
  ## pip install text2vec torch
  from text2vec import Similarity

  a = '如何更换花呗绑定银行卡'
  b = '花呗更改绑定银行卡'

  sim = Similarity()
  s = sim.get_score(a, b)
  print(s)

```

## 计算两个中文句子的相似度 - Option 2

```
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentStore(object):
    def __init__(self, documents):
        self.documents = documents
        # 定制 token pattern, 单个汉字也当作词语，避免单字被忽略
        self.vectorizer = TfidfVectorizer(token_pattern = r"(?u)\b\w+\b")
        self.document_map = {}
        for document in documents:
            words = self.split_word(document)
            self.document_map[document] = words

    @staticmethod
    def split_word(document):
        """
        分词，去除停用词
        """
        stop_words = {":", "的", "，", "”"}

        text = []
        for word in jieba.cut(document):
            if word not in stop_words:
                text.append(word)

        return text

    # 计算两个句子的相似度
    def get_similarity(self, s1, s2):
        # 分词
        words1 = self.document_map.get(s1) if s1 in self.document_map else self.split_word(s1)
        words2 = self.document_map.get(s2) if s2 in self.document_map else self.split_word(s2)

        # 构建TF-IDF向量
        corpus = [' '.join(words1), ' '.join(words2)]
        tfidf = self.vectorizer.fit_transform(corpus)
        # 计算余弦相似度
        sim = cosine_similarity(tfidf[0], tfidf[1])[0][0]
        return sim


    def most_similary_document(self, new_doc):
        score = 0.0
        document = None
        for cur_document in self.documents:
            current_score = self.get_similarity(new_doc, cur_document)
            if current_score > score:
                score = current_score 
                document = cur_document
        return (score, document)

if __name__ == '__main__':

    s1 = '这个苹果很好吃'
    s2 = '这个梨子很好吃'
    store = DocumentStore(["hello", "world"])
    similarity = store.get_similarity(s1, s2)
    print(similarity)

    print("红楼梦的作者是谁: %s" % store.get_similarity("红楼梦的作者是谁","你是谁"))

    print("你是谁: %s" % store.get_similarity("你是谁","你是谁"))
    print("你是谁呀: %s" % store.get_similarity("你是谁呀","你是谁"))
    print("你谁呀: %s" % store.get_similarity("你谁呀","你是谁"))
    print("你是谁？: %s" % store.get_similarity("你是谁？","你是谁"))

    print("你叫什么名字: %s" % store.get_similarity("你叫什么名字","你是谁"))
    print("跟我聊天的人是谁: %s" % store.get_similarity("跟我聊天的人是谁","你是谁"))

```
