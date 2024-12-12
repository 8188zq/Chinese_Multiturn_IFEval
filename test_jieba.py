import jieba
# import nltk
# def count_words(text):
#     """Counts the number of words in Chinese text using jieba."""
#     words = jieba.cut(text)  # 使用jieba进行分词
#     word_list = list(words)  # 将生成的分词结果转换为列表
#     num_words = len(word_list)  # 计算分词后的词数
#     return num_words
# def count_words(text):
#   """Counts the number of words."""
#   tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
#   tokens = tokenizer.tokenize(text)
#   num_words = len(tokens)
#   return num_words

text = "你好，世界！这是一个示例。"
words = jieba.cut(text)
word_list = list(words)
print(word_list)
