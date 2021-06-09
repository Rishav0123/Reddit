import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def depure_data(data):

    regex = re.compile('[^a-zA-Z ]')
    data = regex.sub('', data)
    #Removing URLs with a regular expression
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    data = url_pattern.sub(r'', data)

    # Remove Emails
    data = re.sub('\S*@\S*\s?', '', data)

    # Remove new line characters
    data = re.sub('\s+', ' ', data)

    # Remove distracting single quotes
    data = re.sub("\'", "", data)

    return data

#def stopwords(sen):


stock_fv = pd.read_csv("modified_ref.csv").rename(columns = {"Reff" : "ref_val"})
index_word = pd.read_csv("index_words.csv")
#print(index_word)
#print(word_freq.head())
index_word = index_word.replace(np.nan, ' ', regex=True)

index_word["sentence"] = index_word["title"] +" "+ index_word["text"]
#print(index_word)
d = {}
value = index_word['value']
sentence = index_word['sentence']

for val, sen in zip(value,sentence):
    sen = depure_data(sen)
    d[val] = sen

#sentence = depure_data(sentence)
val_sen = pd.DataFrame(d.items()).rename(columns = {0 : 'val', 1: 'sen'})
#print(val_sen)
#print(type(val_sen))
dir = {}

for v,s in zip(val_sen['val'], val_sen['sen']):
    li = list(s.split(" "))
    dir[v] = li


df = pd.DataFrame(dir.items()).rename(columns = {0 : 'index' , 1 : 'words_l'})
#print(df.info())


#regx = re.compile('[^a-zA-Z ]')
#for words in df['words_l']:
#        conten = regex.sub('', content)

d0 ={}
for ref,term in zip(stock_fv['ref_val'], stock_fv['Term']):
    li = []
    #print(type(ref))
    li = list(ref.split(','))
    #print(li)
    #for val in ref:
    #    print(val)
        #d = df[df['index'] == val]
        #print(d)
    d0[term] = li

term_ref = pd.DataFrame(d0.items()).rename(columns={0:"Stock", 1:"ref_l"})
print(term_ref)
stop_words = set(stopwords.words('english'))
dir_tr = {}
for s,r in  zip(term_ref['Stock'],term_ref['ref_l']):
    li0 = []
    print(r)
    for j in r:
        regex = re.compile("[^0-9]")
        j = regex.sub('',j)
        #print(int(j))
        df0 = df.loc[(df['index'] == int(j))]

        for words in df0['words_l']:
            for word in words:
                word = word.lower()
                if word not in stop_words:
                    li0.append(word)
    dir_tr[s] = li0
    #dir_tr[s] = li0

term_ref = pd.DataFrame(dir_tr.items()).rename(columns={0:"Term", 1:"ref_l"})
print(term_ref)

#term = stock_fv['Term']
#freq = stock_fv['frequency']

dirt1 = {}
#term_freq = pd.DataFrame([term, freq])
term_freq = stock_fv[stock_fv.columns[1:3]]
#term_ref.rename(columns = {2 : "Stock", 3 : "frequency"})
#term_freq.index = ['Stock' , 'freq']

new_df = pd.merge(term_ref, term_freq, on = 'Term')
#for ref in term_ref['ref_l']:
#    for word in ref:
#        print(type(word))
print(new_df)
new_df.to_csv("data.csv")
