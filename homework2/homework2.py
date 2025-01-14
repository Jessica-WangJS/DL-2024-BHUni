# -*- coding: utf-8 -*-
"""homework2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Xi7LIGp6OQ2aNcU-QdNjAcAq2gZ2iWqf
"""

from google.colab import drive
drive.mount('./mount')
# './mount/My Drive/Colab Notebooks/BH/1-2/DL/1/chinese_corpus/'

"""#1"""

import jieba
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

import random
from sklearn.svm import SVC  # 以SVM作为分类器示例
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, accuracy_score
import random
import string
from gensim import corpora, models
from collections import defaultdict

import os

def load_stopwords(file_path):
    stop_words = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        stop_words.extend([word.strip('\n') for word in f.readlines()])
    return stop_words

def preprocess_corpus(text, cn_stopwords):
    for tmp_char in cn_stopwords:
        text = text.replace(tmp_char, "")
    return text

def extract_paragraphs_and_labels(corpus_dict, num_paragraphs, k_value):
    result = []
    total_paragraphs_count = sum(len(corpus_dict[novel]) for novel in corpus_dict)

    if total_paragraphs_count < num_paragraphs:
        print(f"Warning: Only {total_paragraphs_count} paragraphs available in the corpus. Requested {num_paragraphs} will be returned.")
        num_paragraphs = total_paragraphs_count

    # 统计每个小说的段落数量，用于均匀抽取
    paragraph_counts = {novel: len(paragraphs) for novel, paragraphs in corpus_dict.items()}
    # 均匀抽取指定数量的段落
    for _ in range(num_paragraphs):
        # 随机选择一个小说
        novel = random.choices(list(corpus_dict.keys()), weights=[count / total_paragraphs_count for count in paragraph_counts.values()], k=1)[0]
        # 从该小说中随机抽取一个段落
        paragraphs = corpus_dict[novel]
        paragraphs = re.split(r'\n\u3000\u3000', paragraphs)
        paragraph = random.choice(paragraphs)
        # 根据 K 值范围，为该段落选择一个随机的 token 数量
        # 对段落进行截断（如果需要），确保其包含指定数量的 token
        tokens = list(jieba.cut(paragraph))
        result.append((tokens, novel, k_value))
    return result

def LDA(processed_data, num_topics=10):
    X = [item[0] for item in processed_data]  # 段落文本列表
    y = [item[1] for item in processed_data]  # 段落所属小说标签列表

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练LDA模型
    dictionary = corpora.Dictionary(X_train)
    lda_corpus_train = [dictionary.doc2bow(tmp_doc) for tmp_doc in X_train]
    lda = models.LdaModel(corpus=lda_corpus_train, id2word=dictionary, num_topics=num_topics)

    train_topic_distribution = lda.get_document_topics(lda_corpus_train)

    X_train_lda = np.zeros((len(X_train), num_topics))
    for i in range(len(train_topic_distribution)):
        tmp_topic_distribution = train_topic_distribution[i]
        for j in range(len(tmp_topic_distribution)):
            X_train_lda[i][tmp_topic_distribution[j][0]] = tmp_topic_distribution[j][1]

    classifier = SVC(kernel='linear', C=1, random_state=42)
    classifier.fit(X_train_lda, y_train)

    lda_corpus_test = [dictionary.doc2bow(tmp_doc) for tmp_doc in X_test]
    test_topic_distribution = lda.get_document_topics(lda_corpus_test)
    X_test_lda = np.zeros((len(X_test), num_topics))
    for i in range(len(test_topic_distribution)):
        tmp_topic_distribution = test_topic_distribution[i]
        for j in range(len(tmp_topic_distribution)):
            X_test_lda[i][tmp_topic_distribution[j][0]] = tmp_topic_distribution[j][1]

    y_pred = classifier.predict(X_test_lda)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("F1 Score (Macro):", f1_score(y_test, y_pred, average='macro'))

if __name__ == '__main__':
    # 路径设置
    stopwords_file_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/stopwords-zh.txt'
    corpus_folder_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/chinese_corpus/'

    # 加载停用词
    cn_stopwords = load_stopwords(stopwords_file_path)

    # 读取语料库
    corpus_dict = {}  # Dictionary to store novel titles and contents
    for file_name in os.listdir(corpus_folder_path):
        if file_name.endswith('.txt'):
            novel_title = os.path.splitext(file_name)[0]  # Extract novel title from file name
            file_path = os.path.join(corpus_folder_path, file_name)  # Construct full file path
            with open(file_path, 'r', encoding='utf-8') as f:
                novel_content = f.read()
            corpus_dict[novel_title] = novel_content

    # 参数设置
    num_paragraphs = 1000
    k_value = 3000  # Choose the desired token count

    # 定义不同的主题数量
    topic_numbers = [5, 10, 15, 20]

    # 遍历不同的主题数量
    for num_topics in topic_numbers:
        print(f"Results for num_topics = {num_topics}:")

        # 执行主题建模和分类任务
        processed_data = extract_paragraphs_and_labels(corpus_dict, num_paragraphs, k_value)
        LDA(processed_data, num_topics)

"""# 1-1"""

import jieba
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

import random
from sklearn.svm import SVC  # 以SVM作为分类器示例
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, accuracy_score
import random
import string
from gensim import corpora, models
from collections import defaultdict

import os
import pandas as pd

def stopwords(file_path):
    stop_words = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        stop_words.extend([word.strip('\n') for word in f.readlines()])
    return stop_words

def preprocess_corpus(text, cn_stopwords):
    for tmp_char in cn_stopwords:
        text = text.replace(tmp_char, "")
    return text

def extract_paragraphs_and_labels(corpus_dict, num_paragraphs, k_value):
    result = []
    total_paragraphs_count = sum(len(corpus_dict[novel]) for novel in corpus_dict)

    if total_paragraphs_count < num_paragraphs:
        print(f"Warning: Only {total_paragraphs_count} paragraphs available in the corpus. Requested {num_paragraphs} will be returned.")
        num_paragraphs = total_paragraphs_count

    # 统计每个小说的段落数量，用于均匀抽取
    paragraph_counts = {novel: len(paragraphs) for novel, paragraphs in corpus_dict.items()}
    # 均匀抽取指定数量的段落
    for _ in range(num_paragraphs):
        # 随机选择一个小说
        novel = random.choices(list(corpus_dict.keys()), weights=[count / total_paragraphs_count for count in paragraph_counts.values()], k=1)[0]
        # 从该小说中随机抽取一个段落
        paragraphs = corpus_dict[novel]
        paragraphs = re.split(r'\n\u3000\u3000', paragraphs)
        paragraph = random.choice(paragraphs)

        tokens = list(jieba.cut(paragraph))
        result.append((tokens, novel, k_value))
    return result

def LDA(processed_data, num_topics=10):
    X = [item[0] for item in processed_data]  # 段落文本列表
    y = [item[1] for item in processed_data]  # 段落所属小说标签列表

    # 训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练LDA模型
    dictionary = corpora.Dictionary(X_train)
    lda_corpus_train = [dictionary.doc2bow(tmp_doc) for tmp_doc in X_train]
    lda = models.LdaModel(corpus=lda_corpus_train, id2word=dictionary, num_topics=num_topics)

    train_topic_distribution = lda.get_document_topics(lda_corpus_train)

    X_train_lda = np.zeros((len(X_train), num_topics))
    for i in range(len(train_topic_distribution)):
        tmp_topic_distribution = train_topic_distribution[i]
        for j in range(len(tmp_topic_distribution)):
            X_train_lda[i][tmp_topic_distribution[j][0]] = tmp_topic_distribution[j][1]

    classifier = SVC(kernel='linear', C=1, random_state=42)
    classifier.fit(X_train_lda, y_train)

    lda_corpus_test = [dictionary.doc2bow(tmp_doc) for tmp_doc in X_test]
    test_topic_distribution = lda.get_document_topics(lda_corpus_test)
    X_test_lda = np.zeros((len(X_test), num_topics))
    for i in range(len(test_topic_distribution)):
        tmp_topic_distribution = test_topic_distribution[i]
        for j in range(len(tmp_topic_distribution)):
            X_test_lda[i][tmp_topic_distribution[j][0]] = tmp_topic_distribution[j][1]

    y_pred = classifier.predict(X_test_lda)
    report = classification_report(y_test, y_pred, output_dict=True)
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    return {'accuracy': accuracy, 'f1_macro': f1_macro}

if __name__ == '__main__':

    stopwords_file_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/stopwords-zh.txt'
    corpus_folder_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/chinese_corpus/'

    # 加载停用词
    cn_stopwords = stopwords(stopwords_file_path)

    # 读取语料库
    corpus_dict = {}  # Dictionary to store novel titles and contents
    for file_name in os.listdir(corpus_folder_path):
        if file_name.endswith('.txt'):
            novel_title = os.path.splitext(file_name)[0]  # Extract novel title from file name
            file_path = os.path.join(corpus_folder_path, file_name)  # Construct full file path
            with open(file_path, 'r', encoding='utf-8') as f:
                novel_content = f.read()
            corpus_dict[novel_title] = novel_content

    # 参数
    num_paragraphs = 1000
    k_value = 3000  # Choose the desired token count

    # 不同的主题数量
    topic_numbers = [5, 10, 15, 20]

    results = []


    for num_topics in topic_numbers:
        print(f"Results for num_topics = {num_topics}:")


        processed_data = extract_paragraphs_and_labels(corpus_dict, num_paragraphs, k_value)
        result = LDA(processed_data, num_topics)


        results.append({'Num Topics': num_topics, 'Accuracy': result['accuracy'], 'F1 Score (Macro)': result['f1_macro']})


    df = pd.DataFrame(results)


    excel_file_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/classification_results.xlsx'
    df.to_excel(excel_file_path, index=False)

    print("Results saved to Excel file:", excel_file_path)

"""#1-2"""

import jieba
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

import random
from sklearn.svm import SVC  # 以SVM作为分类器示例
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, accuracy_score
import random
import string
from gensim import corpora, models
from collections import defaultdict

import os
import pandas as pd

def load_stopwords(file_path):
    stop_words = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        stop_words.extend([word.strip('\n') for word in f.readlines()])
    return stop_words

def preprocess_corpus(text, cn_stopwords, unit='word'):
    processed_text = ''
    if unit == 'word':
        for tmp_char in cn_stopwords:
            text = text.replace(tmp_char, "")
        processed_text = ' '.join(jieba.cut(text))
    elif unit == 'char':
        processed_text = re.sub(r'\s+', '', text)  # 移除空白字符
    return processed_text

def extract_paragraphs_and_labels(corpus_dict, num_paragraphs, k_value, unit='word'):
    result = []
    total_paragraphs_count = sum(len(corpus_dict[novel]) for novel in corpus_dict)

    if total_paragraphs_count < num_paragraphs:
        print(f"Warning: Only {total_paragraphs_count} paragraphs available in the corpus. Requested {num_paragraphs} will be returned.")
        num_paragraphs = total_paragraphs_count

    paragraph_counts = {novel: len(paragraphs) for novel, paragraphs in corpus_dict.items()}
    # 均匀抽取指定数量的段落
    for _ in range(num_paragraphs):
        # 随机选择一个小说
        novel = random.choices(list(corpus_dict.keys()), weights=[count / total_paragraphs_count for count in paragraph_counts.values()], k=1)[0]
        # 从该小说中随机抽取一个段落
        paragraphs = corpus_dict[novel]
        paragraphs = re.split(r'\n\u3000\u3000', paragraphs)
        paragraph = random.choice(paragraphs)

        if unit == 'word':
            tokens = list(jieba.cut(paragraph))
        elif unit == 'char':
            tokens = list(paragraph)
        result.append((tokens, novel, k_value))
    return result


def LDA(processed_data, num_topics=10):
    X = [item[0] for item in processed_data]  # 段落文本列表
    y = [item[1] for item in processed_data]  # 段落所属小说标签列表

    # 训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练LDA模型
    dictionary = corpora.Dictionary(X_train)
    lda_corpus_train = [dictionary.doc2bow(tmp_doc) for tmp_doc in X_train]
    lda = models.LdaModel(corpus=lda_corpus_train, id2word=dictionary, num_topics=num_topics)

    train_topic_distribution = lda.get_document_topics(lda_corpus_train)

    X_train_lda = np.zeros((len(X_train), num_topics))
    for i in range(len(train_topic_distribution)):
        tmp_topic_distribution = train_topic_distribution[i]
        for j in range(len(tmp_topic_distribution)):
            X_train_lda[i][tmp_topic_distribution[j][0]] = tmp_topic_distribution[j][1]

    classifier = SVC(kernel='linear', C=1, random_state=42)
    classifier.fit(X_train_lda, y_train)

    lda_corpus_test = [dictionary.doc2bow(tmp_doc) for tmp_doc in X_test]
    test_topic_distribution = lda.get_document_topics(lda_corpus_test)
    X_test_lda = np.zeros((len(X_test), num_topics))
    for i in range(len(test_topic_distribution)):
        tmp_topic_distribution = test_topic_distribution[i]
        for j in range(len(tmp_topic_distribution)):
            X_test_lda[i][tmp_topic_distribution[j][0]] = tmp_topic_distribution[j][1]

    y_pred = classifier.predict(X_test_lda)
    report = classification_report(y_test, y_pred, output_dict=True)
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    return {'accuracy': accuracy, 'f1_macro': f1_macro}

if __name__ == '__main__':

    stopwords_file_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/stopwords-zh.txt'
    corpus_folder_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/chinese_corpus/'

    #
    cn_stopwords = load_stopwords(stopwords_file_path)

    # 读取语料库
    corpus_dict = {}  # Dictionary to store novel titles and contents
    for file_name in os.listdir(corpus_folder_path):
        if file_name.endswith('.txt'):
            novel_title = os.path.splitext(file_name)[0]  # Extract novel title from file name
            file_path = os.path.join(corpus_folder_path, file_name)  # Construct full file path
            with open(file_path, 'r', encoding='utf-8') as f:
                novel_content = f.read()
            corpus_dict[novel_title] = novel_content

    # 参数
    num_paragraphs = 1000
    k_value = 3000  # Choose the desired token count

    # 不同的主题数量
    topic_numbers = [5, 10, 15, 20]

    units = ['word', 'char']
    # 不同的基本单元

    results = []  # 存储结果

    # 遍历不同的基本单元
    for unit in units:
        print(f"Results for unit = {unit}:")

        # 遍历不同的主题数量
        for num_topics in topic_numbers:
            print(f"  Results for num_topics = {num_topics}:")

            # 执行主题建模和分类任务
            processed_data = extract_paragraphs_and_labels(corpus_dict, num_paragraphs, k_value, unit=unit)
            result = LDA(processed_data, num_topics)


            results.append({'Unit': unit, 'Num Topics': num_topics, 'Accuracy': result['accuracy'], 'F1 Score (Macro)': result['f1_macro']})


    df = pd.DataFrame(results)

    # 将 DataFrame 保存到 Excel 文件
    excel_file_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/classification_results_with_units.xlsx'
    df.to_excel(excel_file_path, index=False)

    print("Results saved to Excel file:", excel_file_path)

"""# 1-3"""

import jieba
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

import random
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, accuracy_score
import random
import string
from gensim import corpora, models
from collections import defaultdict

import os
import pandas as pd

def load_stopwords(file_path):
    stop_words = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        stop_words.extend([word.strip('\n') for word in f.readlines()])
    return stop_words

def preprocess_corpus(text, cn_stopwords):
    for tmp_char in cn_stopwords:
        text = text.replace(tmp_char, "")
    return text

def extract_paragraphs_and_labels(corpus_dict, num_paragraphs, short_threshold, long_threshold):
    result = []
    total_paragraphs_count = sum(len(corpus_dict[novel]) for novel in corpus_dict)

    if total_paragraphs_count < num_paragraphs:
        print(f"Warning: Only {total_paragraphs_count} paragraphs available in the corpus. Requested {num_paragraphs} will be returned.")
        num_paragraphs = total_paragraphs_count

    # 统计每个小说的段落数量，用于均匀抽取
    paragraph_counts = {novel: len(paragraphs) for novel, paragraphs in corpus_dict.items()}

    # 均匀抽取指定数量的段落
    for _ in range(num_paragraphs):
        # 随机选择一个小说
        novel = random.choices(list(corpus_dict.keys()), weights=[count / total_paragraphs_count for count in paragraph_counts.values()], k=1)[0]
        # 从该小说中随机抽取一个段落
        paragraphs = corpus_dict[novel]
        paragraphs = re.split(r'\n\u3000\u3000', paragraphs)
        paragraph = random.choice(paragraphs)

        tokens = list(jieba.cut(paragraph))

        if len(tokens) <= short_threshold:
            k_value = random.choice(range(short_threshold, long_threshold + 1))
        else:
            k_value = random.choice(range(long_threshold + 1, 2 * long_threshold + 1))

        result.append((tokens, novel, k_value))
    return result

def LDA(processed_data, num_topics=10):
    X = [item[0] for item in processed_data]  # 段落文本列表
    y = [item[1] for item in processed_data]  # 段落所属小说标签列表

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练LDA模型
    dictionary = corpora.Dictionary(X_train)
    lda_corpus_train = [dictionary.doc2bow(tmp_doc) for tmp_doc in X_train]
    lda = models.LdaModel(corpus=lda_corpus_train, id2word=dictionary, num_topics=num_topics)

    train_topic_distribution = lda.get_document_topics(lda_corpus_train)

    X_train_lda = np.zeros((len(X_train), num_topics))
    for i in range(len(train_topic_distribution)):
        tmp_topic_distribution = train_topic_distribution[i]
        for j in range(len(tmp_topic_distribution)):
            X_train_lda[i][tmp_topic_distribution[j][0]] = tmp_topic_distribution[j][1]

    classifier = SVC(kernel='linear', C=1, random_state=42)
    classifier.fit(X_train_lda, y_train)

    lda_corpus_test = [dictionary.doc2bow(tmp_doc) for tmp_doc in X_test]
    test_topic_distribution = lda.get_document_topics(lda_corpus_test)
    X_test_lda = np.zeros((len(X_test), num_topics))
    for i in range(len(test_topic_distribution)):
        tmp_topic_distribution = test_topic_distribution[i]
        for j in range(len(tmp_topic_distribution)):
            X_test_lda[i][tmp_topic_distribution[j][0]] = tmp_topic_distribution[j][1]

    y_pred = classifier.predict(X_test_lda)
    report = classification_report(y_test, y_pred, output_dict=True)
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    return {'accuracy': accuracy, 'f1_macro': f1_macro}

if __name__ == '__main__':
    # 文件路径
    stopwords_file_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/stopwords-zh.txt'
    corpus_folder_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/chinese_corpus/'

    # 停用词
    cn_stopwords = load_stopwords(stopwords_file_path)

    # 语料库
    corpus_dict = {}  # Dictionary to store novel titles and contents
    for file_name in os.listdir(corpus_folder_path):
        if file_name.endswith('.txt'):
            novel_title = os.path.splitext(file_name)[0]  # Extract novel title from file name
            file_path = os.path.join(corpus_folder_path, file_name)  # Construct full file path
            with open(file_path, 'r', encoding='utf-8') as f:
                novel_content = f.read()
            corpus_dict[novel_title] = novel_content

    # 参数
    num_paragraphs = 1000
    short_threshold = 100
    long_threshold = 500
    num_topics = 10

    # 定义不同的 K 值范围
    k_values_short = [20, 50, 100]
    k_values_long = [500, 1000, 2000]

    results = []  # 存储结果

    # 短文本
    for k_short in k_values_short:
        print(f"Results for K (Short Text) = {k_short}:")

        # 执行主题建模和分类任务
        processed_data_short = extract_paragraphs_and_labels(corpus_dict, num_paragraphs, short_threshold, long_threshold)
        result_short = LDA(processed_data_short, num_topics)

        # 存储结果
        results.append({'K (Short Text)': k_short, 'Accuracy (Short Text)': result_short['accuracy'], 'F1 Score (Macro) (Short Text)': result_short['f1_macro']})

    # 长文本
    for k_long in k_values_long:
        print(f"Results for K (Long Text) = {k_long}:")

        # 执行主题建模和分类任务
        processed_data_long = extract_paragraphs_and_labels(corpus_dict, num_paragraphs, short_threshold, long_threshold)
        result_long = LDA(processed_data_long, num_topics)

        # 存储结果
        results.append({'K (Long Text)': k_long, 'Accuracy (Long Text)': result_long['accuracy'], 'F1 Score (Macro) (Long Text)': result_long['f1_macro']})

    # 将结果转换为 DataFrame
    df = pd.DataFrame(results)

    # 将 DataFrame 保存到 Excel 文件
    excel_file_path = './mount/My Drive/Colab Notebooks/BH/1-2/DL/2/topic_model_results.xlsx'
    df.to_excel(excel_file_path, index=False)

    print("Results saved to Excel file:", excel_file_path)