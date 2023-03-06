# by snownlp
import snownlp

text = "学而时习之，不亦说乎at Shanghai China, Windows 2011主席在延安视察"
words = snownlp.SnowNLP(text).words
print(words)


# by pkuseg
import pkuseg

pkuseg.pkuseg(user_dict="dict/sensitive_words.txt")
seg = pkuseg.pkuseg()       # 以默认配置加载模型
words = seg.cut(text)       # 进行分词
print(words)

# by jieba

import jieba

print("segmented result for: %s" % text)
for word in jieba.cut(text, HMM=False):
    print(word)
