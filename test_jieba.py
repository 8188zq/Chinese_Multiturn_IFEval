import jieba

text = "你好，世界！这是一个示例。"
words = jieba.cut(text)
word_list = list(words)
print(word_list)
