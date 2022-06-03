# -*- coding: utf-8 -*-

import pandas as pd
import os

from nltk import PorterStemmer
from collections import defaultdict
import config

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))

import re

class TfIdfCalculator:
  

  @classmethod
  def get_tf_idf(self, msg):
    #self.field = msg.args["field"]
    print(f"msg: {msg}")
    self.df = self.__import_dataset()
    result = self.__calculate_tf_idf(self, self.df)
    return result

    
  def __import_dataset():
    file_root = os.path.join(config.basedir, "test_file") 
    # Read the two excel respectively
    df0 = pd.read_excel(os.path.join(file_root, "PublicEngagement_plat.xlsx") , header=None).iloc[3:,:7]
    df1 = pd.read_excel(os.path.join(file_root, "PublicEngagement_bron.xlsx"), header=None).iloc[3:,:7]
  # Add the new column to record "Rating Level"
    level = []
    for _ in range(len(df0)):
      level.append('Platinum')
    for _ in range(len(df1)):
      level.append('Bronze')

    # Merge the datasets
    df = pd.concat([df0, df1], axis=0, ignore_index=True)
    df.columns = ['School', 'Location', 'Program Type', 'Version', 'Earned Score', 'Total Score', 'Description']
    df['Rated Level'] = level
    df = df.dropna(subset=['Description', 'Rated Level'])
    return df

  def __tokenize(description) -> list:
      tokens = description.split()
      return tokens

  def __stemming(itokens) -> list:
      ps = PorterStemmer()
      tokens = [ps.stem(word) for word in itokens]
      return tokens

  def __remove_stopwords(itokens) -> list:
      tokens = [word for word in itokens if not word in stopwords]
      return tokens

  def __clean_word(word):
    word = word.replace('\"','').replace('\r','').replace('\n','').replace('\t','')
    word = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]", "", word)
    return word

  def __group_by_levels(df) -> dict: # O(n*k) n:length_of_df ; k:length_of_levels
      levels = list(df['Rated Level'].unique())
      dictionary_of_each_level = defaultdict(list)
      for i in range(len(levels)):
          tmp_df_rl = df['Rated Level'].loc[lambda x: x==levels[i]]
          idx_tmp = list(tmp_df_rl.index)
          tmp_df = df['tokens'].loc[idx_tmp]
          for item in tmp_df:
              dictionary_of_each_level[levels[i]] += item
      return dictionary_of_each_level

  def __calculate_tf_idf(self, df):
    df['tokens'] = [self.__remove_stopwords(self.__stemming([self.__clean_word(j) for j in self.__tokenize(i)])) for i in df['Description']]
    #print(df['tokens'])

    dict_levels = self.__group_by_levels(df)
    #print(dict_levels)
    #for item in dict_levels:
    #  dict_levels[item] = (' ').join(dict_levels[item])

    from nltk import FreqDist
    words_count = list()
    for doc in dict_levels:
      TF = FreqDist(dict_levels[doc])
      words_count.append(TF)

    def dict_TF(words_count):
      TF_doc = list()
      for i in range(len(words_count)):
        tmp_TF = dict()
        words_in_doc = words_count[i]
        all_count = 0
        for word in words_in_doc:
          all_count += words_in_doc[word]
        for word in words_in_doc:
          tmp_TF[word] = words_in_doc[word]/all_count
        TF_doc.append(tmp_TF)
      return TF_doc

    TF_doc = dict_TF(words_count)
    len(TF_doc)

    def tf(term, token_doc):
        tf = token_doc.count(term)/len(token_doc)
        return tf

    import math
    def numDocsContaining(word, token_doclist):
        doccount = 0
        for doc_token in token_doclist:
            if doc_token.count(word) > 0:
                doccount +=1
        return doccount

    def idf(word, token_doclist):
        n = len(token_doclist)
        df = numDocsContaining(word, token_doclist)
        return math.log10(n/df)

    import operator

    #calculate tfidf
    doc_all = dict_levels

    #create bag words
    bag_words =[] # declare bag_words is a list
    for doc in doc_all.keys():
      bag_words += doc_all[doc]
    bag_words=set(bag_words)
    #print(bag_words)

    #calculate idf for every word in bag_words
    bag_words_idf={} # declare "bag_words_idf" data structure is dictionary 
    for word in bag_words:
      bag_words_idf[word]= idf(word,doc_all.values())
    #print(bag_words_idf)

    tfidf={} # declare tfidf dictionary to store tfidf value
    for doc in doc_all.keys():
      tfidf_doc={} # delare tfidf_doc as a dictionary to store tfidf of each doc
      for term in set(doc_all[doc]):
        tfidf_doc[term]= tf(term,doc_all[doc]) * bag_words_idf[term] # calculate tfidf for each doc
      # Sort tfidf by value
      tfidf_doc = dict(sorted(tfidf_doc.items(), key=operator.itemgetter(1),reverse=True))
      tfidf[doc]= tfidf_doc

    tf_dataframe = pd.DataFrame(tfidf).transpose()

    tf_idf_token_dict = {}
    for index, row in tf_dataframe.iterrows():
      tf_idf_token_dict[index] = list(row.sort_values(ascending=False)[:49].to_dict().keys())

    # for each category, get first 50 token
    # give json
    import json
    tf_idf_token_json = json.dumps(tf_idf_token_dict, indent = 4)

    #with open('tf_idf_seed.json', 'w') as outfile:
    #  print("outfile.write(tf_idf_token_json)\n")
    #  outfile.write(tf_idf_token_json)
        

    return tf_idf_token_json
