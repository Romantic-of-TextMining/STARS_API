#Mount google drive to google colab virtual machine
from google.colab import drive
drive.mount('/content/drive')
mydrive ="/content/drive/My Drive/Colab Notebooks/"

def download_data_gdown(path,file_id):
    import gdown, os, zipfile, sys
    url = f"https://drive.google.com/uc?id={file_id}"
    data_zip = os.path.join(path, "pdf.zip")
    gdown.download(url, data_zip, quiet=False)
    
    with zipfile.ZipFile(data_zip, "r") as zip_ref:
        zip_ref.extractall(path)
    return
download_data_gdown(path=mydrive,file_id="1_A2szoWp5dTdsJ0COtyreE9ZpEtW_xuf")

#Mount google drive to google colab virtual machine
from google.colab import drive
drive.mount('/content/drive')
mydrive ="/content/drive/My Drive/Colab Notebooks/"

## File checking function

## Write data if txt file exists
def file_exist_write(myDir,myFilename,text):
  textFilename = myDir+myFilename
  if not os.path.isfile(textFilename): # Check if the txt file exists
    textFile = open(textFilename, "w") #make text file
    textFile.write(text) #write text to text file
    textFile.close()
    print("finish convert to txt, skip ", myFilename)
  else:
    print("Txt file already exists", myFilename)

## Check if file exist or not
def file_exist(myDir,myFilename):
  textFilename = myDir+myFilename
  if not os.path.isfile(textFilename): # Check if the txt file exists
    return False
  else:
    return True

#Run to load pdf to txt function
!pip3 install pdfminer.six #package pdf to text
import os
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text    
        
def convertMultiple(pdfDir, txtDir):
    for pdf in os.listdir(pdfDir): #iterate through pdfs in pdf directory
        NameRule=r'[a-zA-Z]+_[a-zA-Z]+-[0-9]+_[a-zA-Z ]+.pdf'
        try:
          pdf=re.search(NameRule,pdf).group()
          fileExtension = pdf.split(".")[-1]
          if fileExtension == "pdf":
            pdfFilename = pdfDir + pdf 
            convertText = convert(pdfFilename) #get string of text content of pdf
            textFilename = pdf[:-4] + ".txt"
            file_exist_write(txtDir,textFilename,convertText)
        except:
          print(f"The name of pdf {pdf} causes AttributeError, please follow the NameRule=r'[a-zA-Z]+_[a-zA-Z]+-[0-9]+_[a-zA-Z ]+.pdf'")
          print("for example:Platinum_EN-14_international level.pdf")
    print("finish convert all file")

#create directory txt
#os.mkdir(mydrive+ 'txt') # you have to remove this line if the txt folder is exist.
# covert all file in folder pdf to text file and store in folder "txt"
mydrive ="/content/drive/My Drive/Colab Notebooks/"
os.makedirs(mydrive+"txt",exist_ok=True) #make txt folder to save text file after convert pdf to txt
pdfdir= mydrive + "pdf/"
txtdir= mydrive +"txt/"
convertMultiple(pdfdir,txtdir)

# create tf function
def tf(term, token_doc):
    tf = token_doc.count(term)/len(token_doc)
    return tf

# create function to calculate how many doc contain the term 
def numDocsContaining(word, token_doclist):
    doccount = 0
    for doc_token in token_doclist:
        if doc_token.count(word) > 0:
            doccount +=1
    return doccount
  
import math
# create function to calculate  Inverse Document Frequency in doclist - this list of all documents
def idf(word, token_doclist):
    n = len(token_doclist)
    df = numDocsContaining(word, token_doclist)
    return math.log10(n/df)

#define a function to do cosine normalization a data dictionary
def cos_norm(dic): # dic is distionary data structure
  import numpy as np
  dic_norm={}
  factor=1.0/np.sqrt(sum([np.square(i) for i in dic.values()]))
  for k in dic:
    dic_norm[k] = dic[k]*factor
  return dic_norm

#create function to calculate normalize tfidf 
def compute_tfidf(token_doc,bag_words_idf):
  tfidf_doc={}
  for word in set(token_doc):
    tfidf_doc[word]= tf(word,token_doc) * bag_words_idf[word]   
  tfidf_norm = cos_norm(tfidf_doc)
  return tfidf_norm

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

def compute_tfidf_query(query_token,bag_words_idf):
  tfidf_query={}
  tf_norm_query = tf_norm(query_token)
  for term, value in tf_norm_query.items():
    tfidf_query[term]=value*bag_words_idf[term]   
  return tfidf_query

  #install wget if you not yet install wget
!pip install wget
#Download jieba big dictionary from github
import wget,os
#os.mkdir(mydrive+ "chinese") # you have to remove this line if the chinese folder is exist.
url_bigdict = 'https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big'
wget.download(url_bigdict, mydrive)

import re # Import regular Expression Package to deal with term 

def clean_word(word):
  word = word.replace('\"','').replace('\r','').replace('\n','').replace('\t','')
  word = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]", "",word)
  return word

#download chinese stopwords file at https://raw.githubusercontent.com/stopwords-iso/stopwords-zh/master/stopwords-zh.txt
# and save to your computer, you also add more chinese stopwords
import requests

!pip3 install opencc-python-reimplemented
from opencc import OpenCC
cc = OpenCC('s2t')

#url = 'https://raw.githubusercontent.com/stopwords-iso/stopwords-zh/master/stopwords-zh.txt'
#r = requests.get(url, allow_redirects=True)
#open('chinese_stopwords.txt', 'wb').write(r.content)

url = 'https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big'
r = requests.get(url, allow_redirects=True)

open('dict.txt.big', 'wb').write(r.content)

zh_stopwords_path="dict.txt.big"
zh_stopwords_path = [cc.convert(line.strip()) for line in open(zh_stopwords_path, 'r', encoding='utf-8').readlines()]

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
## Merge chinese stopwords and english stopwords
en_stopwords = stopwords.words('english')
stopwords= zh_stopwords_path + en_stopwords

len(stopwords)

# The data return from CKIP is in multiple level structure, so I have to transform it into 1 tier list

flat_list = list()
def flatten_list(list_of_lists): # This function is iterative function, which means it will call itself iteratively. 
    for item in list_of_lists:
        if type(item) == list:
            flatten_list(item)
        else:
            flat_list.append(item)  
    return flat_list

## Create data snapshot function
import json

dest_dir = mydrive+"pdf/"

def doc_save_to_json_file(dest_dir,myfilename,mydata):
  dest_file = dest_dir+myfilename
 # print("dest_file",dest_file)
 # print("myfilename",myfilename)

  if not os.path.isfile(dest_file):
    if not os.path.isdir(dest_dir):
      os.makedirs(dest_dir, mode=0o777)

    with open(dest_file,'w', encoding='utf-8') as file:
      json.dump(mydata, file, indent = 4)

  else:
    with open(dest_file,'w', encoding='utf-8') as file:
      json.dump(mydata, file, indent = 4)


def doc_read_json(dest_dir,dest_filename):
  dest_dir = dest_dir
  dest_file = dest_dir+myfilename
 # print("dest_file",dest_file)
 # print("myfilename",myfilename)

  myJsonFileLoc = dest_dir+dest_filename
  if os.path.isfile(myJsonFileLoc):
    with open(myJsonFileLoc) as outfile:
      json_data = json.load(outfile)
  else:
    json_data = []
  return json_data

# this code will read all file in txt folder, tokenize using jieba, remove punctuation, remove stopword and combine all file into doc_all
#import jieba,os
#jieba.load_userdict(mydrive + "dict.txt.big")

file_path = mydrive +"txt/"
doc_all_2={}
# Our unit of analysis is "document(pdf)"
for filename in os.listdir(file_path ):
  fileExtension = filename.split(".")[-1]
  if fileExtension == "txt":
    chinese_text = open(file_path+filename).read()
    text = [p for p in chinese_text.split('\n') if len(p) != 0]
    myfilename = filename.replace(".txt",".json")
    print(file_path+'json/'+myfilename)

    if(not file_exist(file_path+'json/',myfilename)): # file_exist(file_path+'json/',myfilename)
      #tokens = list(jieba.cut(text))
      tokens  = list(ws_driver(text, use_delim=True, batch_size=256, max_length=128))
      flat_list = list()
      tokens = flatten_list(tokens)

      token_filtered = [clean_word(w) for w in tokens if len(w)>1 and not w in stopwords] # Skip words in stopwords
      doc_all_2[filename[:-4]]=token_filtered
      doc_save_to_json_file(file_path+'json/',myfilename,token_filtered)

      print(token_filtered)
      #print('JSON File does not exist')
    else:
      print(myfilename,'already exist in json directory')
      doc_all_2[filename[:-4]] = doc_read_json(file_path+'json/',myfilename)
#    break

#create bag words
bag_words_2 =[] # declare bag_words is a list
for doc in doc_all_2.keys():
  bag_words_2 += doc_all_2[doc]
bag_words_2
print(bag_words_2)
input_vocabulary=[]
for inputvocabulary in bag_words_2:
 inputvocabulary ="".join(re.findall('[a-zA-Z]|[^0-9]', str(inputvocabulary))) #至少先刪掉長得像網址的斷句
 if inputvocabulary != "":
    input_vocabulary.append(inputvocabulary)
print(input_vocabulary)
bag_words_frequency=input_vocabulary
bag_words_2=set(bag_words_2)


#calculate idf for every word in bag_words
bag_words_idf_2={} # declare "bag_words_idf" data structure is dictionary 
for word in bag_words_2:
  bag_words_idf_2[word]= idf(word,doc_all_2.values())

##calculate tfidf with cosine normalization
tfidf_2={} # declare tfidf dictionary to store tfidf value
for doc in doc_all_2.keys():
  tfidf_2[doc]= compute_tfidf(doc_all_2[doc],bag_words_idf_2)

from nltk.probability import FreqDist
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))
filtered_tokens = [word for word in bag_words_frequency if not word in stopwords]
user_stopwords = ["'s",".","ca","'",'"',":","-","~","(",")","$","&","“","”","–","’",",","1","2","%","In","For","The","also","‧","．","·","•",""]
filtered_tokens_2 = [word for word in filtered_tokens if not word in user_stopwords]

import re
query_2 = "enter"
query_token_raw_2 = (ws_driver(query_2, use_delim=True, batch_size=256, max_length=128))

flat_list = list()
query_token_raw_2 = flatten_list(query_token_raw_2)

query_token_2 = set(query_token_raw_2).intersection(bag_words_2)
tfidf_query_2 =compute_tfidf_query(list(query_token_2),bag_words_idf_2)
import pandas as pd
Cos_score = pd.DataFrame(tfidf_2).transpose()
Cos_score= Cos_score.fillna(0)

#將跑好的數值儲存成.csv在雲端
from google.colab import drive

drive.mount('/content/drive')
path = '/content/drive/MyDrive/output.csv'

with open(path, 'w', encoding = 'utf-8-sig') as f:
  Cos_score.to_csv(f)

#運用檔案在雲端的位置讀取該檔
import pandas as pd
data = pd.read_csv('/content/drive/MyDrive/output.csv') 

#輸入一個想要查詢的字，呈現其分數之於各檔案
want_to_know=input("請輸入您想知道的單字")
print("="*47)
df = pd.DataFrame(data,columns=["Unnamed: 0",want_to_know])
df.columns = df.columns.str.replace('Unnamed: 0','FileName')
print (df)
