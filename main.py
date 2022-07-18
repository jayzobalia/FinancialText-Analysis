import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
import warnings

warnings.filterwarnings('ignore')
from nltk.tokenize import word_tokenize, sent_tokenize

global web_links


class DataExtraction():
    def __init__(self):
        web_links_df = pd.read_csv('Input.csv')
        self.soups = []
        self.urls = web_links_df['URL']
        self.url_id = web_links_df['URL_ID']
        self.stop_word_list = []
        self.positive_word_list = []
        self.negative_word_list = []
        self.positive_score = []
        self.negative_score = []
        self.polarity_score = []
        self.subjectivity_score = []
        self.avg_sentence_length = []
        self.percentage_complex_words = []
        self.avg_syllable_per_word = []
        self.fog_index = []
        self.complex_word_count = []
        self.avg_word_length = []
        self.word_count = []
        self.personal_pronouns_count = []

    def get_data(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36'}
        for i in range(len(self.urls)):
            blog = requests.get(self.urls[i], headers=headers)
            html_content = blog.content
            soup = BeautifulSoup(html_content, 'html.parser')
            mydivs = soup.findAll('div', class_="td-post-content")
            for div in mydivs:
                string = div.get_text()
                file_name = "text_files\\" + str(self.url_id[i]) + ".txt"
                with open(file_name, 'w', encoding="utf-8") as f:
                    f.write(string)

    def get_stop_words(self):
        text_file_names = ['StopWords_Auditor.txt', 'StopWords_Currencies.txt', 'StopWords_DatesandNumbers.txt',
                           'StopWords_Generic.txt', 'StopWords_GenericLong.txt', 'StopWords_Geographic.txt',
                           'StopWords_Names.txt']

        for i in range(len(text_file_names)):
            file_name = 'StopWords/' + text_file_names[i]
            with open(file_name) as f:
                contents = f.readlines()
                for i in contents:
                    i = i[0:-1]
                    self.stop_word_list.append(i)

        self.stop_word_list = sorted(self.stop_word_list)

    def remove_stop_words(self):
        custom_stopwords = self.stop_word_list
        for i in range(1, len(self.url_id) + 2):
            if i != 44:
                file_name = 'text_files/' + str(i) + '.txt'
                new_file_name = 'text_files_cleaned/' + str(i) + '_cleaned.txt'

            with open(file_name, 'r', encoding="utf-8") as f:
                new_string = f.read()
                text_tokens = word_tokenize(new_string)
                fin_string_list = [word for word in text_tokens if not word in custom_stopwords]
                fin_string = " ".join(fin_string_list)
                fin_string = re.sub('[^a-zA-Z.]', ' ', fin_string)
                fin_string = re.sub('\\s+', ' ', fin_string)
                f.close()

            with open(new_file_name, 'w', encoding="utf-8") as k:
                k.write(fin_string)
                k.close()

    def get_Master_Dicornary(self):

        with open('Master_Dictionary/positive-words.txt', 'r') as f:
            pos_words = f.readlines()
            for i in pos_words:
                i = i[0:-1]
                if i in self.stop_word_list:
                    pass
                else:
                    self.positive_word_list.append(i)
        f.close()

        with open('Master_Dictionary/negative-words.txt', 'r') as k:
            neg_words = k.readlines()
            for i in neg_words:
                i = i[0:-1]
                if i in self.stop_word_list:
                    pass
                else:
                    self.negative_word_list.append(i)
        f.close()

    def pos_neg_variables(self):
        for i in range(1, len(self.urls) + 2):
            if i != 44:
                file_name = 'text_files_cleaned/' + str(i) + '_cleaned.txt'
                with open(file_name, 'r', encoding="utf-8") as f:
                    new_string = f.read()
                    words = word_tokenize(new_string)
                    count_pos = 0
                    count_neg = 0
                    for word in words:
                        if (word in self.positive_word_list):
                            count_pos = count_pos + 1
                        if (word in self.negative_word_list):
                            count_neg = count_neg + 1

                    self.positive_score.append(count_pos)
                    self.negative_score.append(count_neg)
                    self.polarity_score.append((count_pos - count_neg) / ((count_pos + count_neg) + 0.000001))
                    self.subjectivity_score.append((count_pos + count_neg) / (len(words) + 0.000001))
                f.close()

    def readablitiy(self):
        for i in range(1, len(self.urls) + 2):
            if i != 44:
                file_name = 'text_files_cleaned/' + str(i) + '_cleaned.txt'
                with open(file_name, 'r', encoding="utf-8") as f:
                    new_string = f.read()
                    words = word_tokenize(new_string)
                    sentances = sent_tokenize(new_string)
                    avg_sentance_length = (len(words) - len(sentances)) / len(sentances)

                    countx = 0
                    for i in range(0, len(new_string)):
                        if (new_string[i] != ' ' and new_string[i] != '.'):
                            countx = countx + 1

                    syllable_per_word = []
                    for word in words:
                        if word != '.':
                            word = word.lower()
                            count = 0
                            vowels = "aeiouy"
                            if word[0] in vowels:
                                count += 1
                            for index in range(1, len(word)):
                                if word[index] in vowels and word[index - 1] not in vowels:
                                    count += 1
                            if word.endswith("e"):
                                count -= 1
                            if count == 0:
                                count += 1
                            syllable_per_word.append(count)

                    cnt = 0
                    for k in range(len(syllable_per_word)):
                        if syllable_per_word[k] > 2:
                            cnt = cnt + 1

                    percentage_complex = 100 * cnt / (len(words) - len(sentances))
                    avg_syllable_per_word = sum(syllable_per_word) / (len(words) - len(sentances))

                    self.avg_sentence_length.append(avg_sentance_length)
                    self.word_count.append(len(words))
                    self.avg_word_length.append(countx / (len(words) - len(sentances)))
                    self.complex_word_count.append(cnt)
                    self.percentage_complex_words.append(percentage_complex)
                    self.avg_syllable_per_word.append(avg_syllable_per_word)
                    self.fog_index.append(0.4 * avg_sentance_length + percentage_complex)

    def personal_pronouns(self):
        for i in range(1, len(self.urls) + 2):
            if i != 44:
                file_name = 'text_files/' + str(i) + '.txt'
                with open(file_name, 'r', encoding="utf-8") as f:
                    text = f.read()
                    tokens = word_tokenize(text)
                    cntt = 0

                    for q in tokens:
                        if (q == 'I' or q == 'we' or q == 'my' or q == 'our' or q == 'ours' or q == 'us'):
                            cntt = cntt + 1

                    self.personal_pronouns_count.append(cntt)

    def output_csv(self):
        URL_ID = self.url_id
        URL = self.urls
        positive_score = self.positive_score
        negative_score = self.negative_score
        polarity_score = self.polarity_score
        subjectivity_score = self.subjectivity_score
        avg_sentance_length = self.avg_sentence_length
        percentage_complex_words = self.percentage_complex_words
        fog_index = self.fog_index
        avg_words_per_sentance = self.avg_sentence_length
        complex_word_count = self.complex_word_count
        word_count = self.word_count
        syllable_per_word = self.avg_syllable_per_word
        personal_pronouns = self.personal_pronouns_count
        avg_word_length = self.avg_word_length

        data = {'URL_ID': pd.Series(URL_ID), 'URL': pd.Series(URL), 'POSITIVE SCORE': pd.Series(positive_score),
                'NEGATIVE SCORE': pd.Series(negative_score), 'POLARITY SCORE': pd.Series(polarity_score),
                'SUBJECTIVITY SCORE': pd.Series(subjectivity_score), 'AVG SENTENCE LENGTH': pd.Series(avg_sentance_length),
                'PERCENTAGE OF COMPLEX WORDS': pd.Series(percentage_complex_words), 'FOG INDEX': pd.Series(fog_index),
                'AVG NUMBER OF WORDS PER SENTANCE': pd.Series(avg_words_per_sentance),
                'COMPLEX WORD COUNT': pd.Series(complex_word_count), 'WORD COUNT': pd.Series(word_count),
                'SYLLABLE PER WORD': pd.Series(syllable_per_word), 'PERSONAL PRONOUNS': pd.Series(personal_pronouns),
                'AVG WORD LENGTH' : pd.Series(avg_word_length)
                }
        df = pd.DataFrame(data)

        df.to_csv('C:\\Users\\jayzo\\PycharmProjects\\Data_Extraction_and_Text_Analysis\\output.csv')


obj = DataExtraction()
obj.get_Master_Dicornary()
obj.pos_neg_variables()
obj.readablitiy()
obj.personal_pronouns()
obj.output_csv()
