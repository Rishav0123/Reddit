import praw
import pandas as pd
import re
import requests
import heapq

reddit = praw.Reddit(client_id='1p1TFZRaTsRbgQ', client_secret='wtPo5WoUI17a5VJwwLfFMMy4zWeBvA', user_agent='Rishav Dutta')
stocks = pd.read_csv("/home/elliot/Desktop/reddit/nasdaq_screener_1622817397825.csv").rename(columns={"Symbol":"Term"})
#stocks["Term"] = stocks["Term"]+ stocks["Symbol"]
stock_names = stocks["Term"]
#print(stock_names)
#hot_post=[]
df = []
k=0

for post in reddit.subreddit('wallstreetbets').hot(limit=500):
    content = {
    "title" : post.title,
    "text" : post.selftext,
    "value" : k
    }
    df.append(content)
    k=k+1
df = pd.DataFrame(df)
#print(df)
df.to_csv('index_words.csv')
#for names in stock_names:
#hot_post = reddit.subreddit('Stocks').hot(limit=10)
regex = re.compile('[^a-zA-Z ]')
word_dict = {}
reff_dict = {}
list = []

for (index, row) in df.iterrows():
    value = row['value']
    #print(type(value))
    #title
    title = row['title']
    title = regex.sub('', title)
    title_words = title.split(' ')
    #title_words['value'] = row['value']
    #title_words = {'words_t' : title_words, 'value' : value }
    #title_words = pd.DataFrame(title_words)
    #title_keyvalue = {'title_words' : title_words , 'value' : row['value']}
    #print(title_keyvalue)

    #content
    content = row['text']
    content = regex.sub('', content)
    content_words = content.split(' ')
    #content_keyvalue = {'content_words' : content_words , 'value' : row['value']}

    #combine
    words = title_words + content_words
    words_keyvalue = {'word' : words , 'word_keyvalue' : row['value']}
    #print(words_keyvalue)
    #print(words)


    for x in words:

        if x in ['A', 'B', 'GO', 'ARE', 'ON']:
            pass

        elif x in word_dict:
            word_dict[x] += 1
            reff_dict[x].append(value)
            #new2 = list[x].append(value)
            #word_dict[x] = word_dict[x] + {}

        else:
            li = []
            word_dict[x] = 1
            li.append(value)
            reff_dict[x] = li
            #new1 = list[x].append(value)
            #x.list
            #word_dict[x] = word_dict[x] + {'value' : row['value']}

#print(word_dict)
word_df = pd.DataFrame.from_dict(word_dict.items()).rename(columns = {0:"Term", 1:"frequency"})
reff_df = pd.DataFrame.from_dict(reff_dict.items()).rename(columns = {0: "Term",1:"reference"})
reff_df.to_csv("test.csv")

word_df = pd.merge(word_df, reff_df, on="Term")
#print(word_df)


merged_df = pd.merge(word_df, stock_names, on="Term")


#x = merged_df['reference']
#print(x)
dict0 = {}
for term, ref in zip(merged_df['Term'], merged_df['reference']):

    res = []
    for x in ref :
        if x not in res:
            print(x)
            res.append(x)
    dict0[term] = res
#merged_df['reff_df'] =
#print(dict0)
dfn = pd.DataFrame.from_dict(dict0.items()).rename(columns = {0: "Term", 1:"Reff"})
#merged_df.to_csv("merged.csv")
#n_merged = merged_df.drop(['reference'])
#term = merged_df['Term']
#freq = merged_df['frequency']
new_df = merged_df[merged_df.columns[0:2]]


#for post in hot_post:
#    posts.append([post.title])
#print(new_df.info())

dfn = pd.merge(new_df, dfn, on="Term")
print(dfn)
dfn.to_csv("modified_ref.csv")

#posts = pd.DataFrame(posts,columns=['title'])
#posts["index"] = posts['title'].str.find(stock_names)
