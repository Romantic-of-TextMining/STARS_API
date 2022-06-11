# get doc_all_2 as doc -> token
# get bag_words_2 from doc_all_2
# bag_words_idf_2 get key as doc_all_2, value from idf
# tfidf_2 as tdidf for each file
# get cos from query and tfidf_2
import math
import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine
import json

from adapters import gateway 
from domain import tf_idf

class CosSimCalCulator:

    @classmethod
    def get_cos_sim_by_query(self, msg):
        self.field = msg["field"]
        self.query = msg["query"]

        self.field_dict = gateway.FieldSheet(self.field).get_items_from_field()
        self.__calculate_field_tfidf(self)
        result_dict = self.__calculate_query_cos_sim(self)
        result = json.dumps(result_dict, indent = 4)

        return result

    def __calculate_field_tfidf(self):
        self.__restructure_items(self)
        self.__preprocess(self)

    def __restructure_items(self):
        self.items_dict = {}
        self.bag_words = []
        for level, level_dict in self.field_dict["Rated Level"].items():
            for filename, filename_dict in level_dict.items():
                name = f"{level}__{filename}"
                self.items_dict[name] = []
                #self.field_dict['Rated Level']['bronze']['public_engagement']['token']
                for description in filename_dict['Description']:
                    token = tf_idf.TfIdfCalculator.pre_process2token(description)
                    self.items_dict[name]+=token
                self.bag_words+=self.items_dict[name]
        self.bag_words = set(self.bag_words)

    def __preprocess(self):
        self.bag_words_idf={}
        for token in self.bag_words:
            self.bag_words_idf[token]= CosSimLib.idf(token, self.items_dict.values())

        self.tfidf={} # declare tfidf dictionary to store tfidf value
        for doc in self.items_dict.keys():
            self.tfidf[doc]= CosSimLib.compute_tfidf(self.items_dict[doc], self.bag_words_idf)

    def __calculate_query_cos_sim(self):

        self.query_token = tf_idf.TfIdfCalculator.pre_process2token(self.query)
        
        query_token = set(self.query_token).intersection(self.bag_words)
        tfidf_query =CosSimLib.compute_tfidf_query(list(query_token), self.bag_words_idf)
        #calculate tfidf for query text

        # add tfidf of query text to tfidf of all doc and convert to dataframe
        self.tfidf["query"]=tfidf_query
        tfidf_df = pd.DataFrame(self.tfidf).transpose()
        tfidf_df= tfidf_df.fillna(0) # replace all NaN by zero
        cosine_sim ={}
        for row in tfidf_df.index:
            if row != "query":
                cosine_sim[row]= 1-cosine(tfidf_df.loc[row],tfidf_df.loc["query"])

        cosine_sim = dict(sorted(cosine_sim.items(), key=lambda item: item[1],reverse=True))
        return cosine_sim

class CosSimLib:

    @classmethod
    # create tf function
    def tf(self, term, token_doc):
        tf = token_doc.count(term)/len(token_doc)
        return tf

    @classmethod
    # create function to calculate  Inverse Document Frequency in doclist - this list of all documents
    def idf(self, word, token_doclist):
        n = len(token_doclist)
        df = self.__numDocsContaining(word, token_doclist)
        return math.log10(n/df)

        #create function to calculate normalize tfidf
    @classmethod
    def compute_tfidf(self, token_doc,bag_words_idf):
        tfidf_doc={}
        for word in set(token_doc):
            tfidf_doc[word]= self.tf(word, token_doc) * bag_words_idf[word]   
        tfidf_norm = self.__cos_norm(tfidf_doc)
        return tfidf_norm

    @classmethod
    def compute_tfidf_query(self, query_token,bag_words_idf):
        tfidf_query={}
        tf_norm_query = self.tf_norm(query_token)
        for term, value in tf_norm_query.items():
            tfidf_query[term]=value*bag_words_idf[term]   
        return tfidf_query

    # create function to calculate how many doc contain the term 
    def __numDocsContaining(word, token_doclist):
        doccount = 0
        for doc_token in token_doclist:
            if doc_token.count(word) > 0:
                doccount +=1
        return doccount

    #define a function to do cosine normalization a data dictionary
    def __cos_norm(dic): # dic is distionary data structure
        dic_norm={}
        factor=1.0/np.sqrt(sum([np.square(i) for i in dic.values()]))
        for k in dic:
            dic_norm[k] = dic[k]*factor
        return dic_norm

    # create normalize term frequency
    def tf_norm(token_doc):
        tf_norm={}
        for term in token_doc:
            tf = token_doc.count(term)/len(token_doc)
            tf_norm[term]=tf
        try: 
            tf_max =max(tf_norm.values())
        except:
            pass
        for term, value in tf_norm.items():
            tf_norm[term]= 0.5 + 0.5*value/tf_max
        return tf_norm

"""
get all_item_and_token by
    get json from each file
    get token from json, name with item and level
"""

"""
from adapters import gateway 
from domain import cos_sim
msg = {}
msg["field"] = "en_14_participation_in_public_policy"
msg["query"] = "expand good ambassador"
result = cos_sim.CosSimCalCulator.get_cos_sim_by_query(msg)
"""