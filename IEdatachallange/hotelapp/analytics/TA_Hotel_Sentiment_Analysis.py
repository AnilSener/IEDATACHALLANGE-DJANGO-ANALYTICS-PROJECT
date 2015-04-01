# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:10:26 2015

@author: root
"""

import pymongo
import gc
from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score
import random
from pandas import concat
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import itertools
from nltk.corpus import sentiwordnet as swn

from hotelapp.models import HotelReview,HotelSentiment
#from django_pandas.io import read_frame
import configparser
config = configparser.ConfigParser()
config.read('../../app.conf')
from mongoengine.connection import connect,disconnect
connection=connect(config["MONGODB"]["DB_NAME"])

wnl = nltk.WordNetLemmatizer()


df = pd.DataFrame(list(HotelReview.objects.values_list( "id","review","title","rating")),columns=["id","review","title","rating"])
#df = pd.DataFrame(list(reviews.find({"review":{"$exists":"true"}}, {"review": 1, "rating": 1, "_id":0})))
#df['Senti_Score'] = 0
#print(df)
def conv_pos(x):
    if x[:2] == 'NN':
        return 'n';
    elif x[:2] == 'JJ':
        return 'a';
    elif x[:1] == 'V':
        return 'v';
    elif x[:1] == 'R':
        return 'r';
    else:
        return None;

for i,review in enumerate(df["review"]):
    print(i)


    review=review.replace("\n","")
    df["title"][i]=df["title"][i].replace("\n","")
    sentences = nltk.sent_tokenize(review)
    title_sentences = nltk.sent_tokenize(df["title"][i])
    stokens = [nltk.word_tokenize(sent) for sent in sentences]
    title_stokens = [nltk.word_tokenize(sent) for sent in title_sentences]
    taggedlist=[]
    title_taggedlist=[]
    for stoken in stokens:
        taggedlist.append(nltk.pos_tag(stoken))
    for title_stoken in title_stokens:
        title_taggedlist.append(nltk.pos_tag(title_stoken))
    #stokens = list(itertools.chain(*stokens))
    #print(taggedlist)
    score_list=[]
    title_score_list=[]
    cnt=0
    for idx,taggedsent in enumerate(taggedlist):
        score_list.append([])

        for idx2,t in enumerate(taggedsent):
            newtag=conv_pos(t[1])
            lemmatized=wnl.lemmatize(t[0])
            #Adding Review Word Record
            rev_word=HotelSentiment()
            cnt+=1
            rev_word.seq_no=cnt
            rev_word.reviewID=HotelReview.objects.get(id=df['id'].loc[i])
            rev_word.type="review"
            rev_word.lemma_word=lemmatized
            rev_word.word=t[0]
            rev_word.pos_tag=t[1]
            if(newtag!=None):
                synsets = list(swn.senti_synsets(lemmatized, newtag))

                #print(synsets)
                #score=0
                if(len(synsets)>0):
                    #score=synsets[0].pos_score()-synsets[0].neg_score()
                    rev_word.pos_senti_score=synsets[0].pos_score()
                    rev_word.neg_senti_score=synsets[0].neg_score()
                    rev_word.obj_senti_score=synsets[0].obj_score()
                    #score_list[idx].append(synsets[0].pos_score())
                    #score_list[idx].append(synsets[0].neg_score())
            rev_word.save()
            #print(title_taggedlist)
    cnt=0
    for idx,taggedsent in enumerate(title_taggedlist):
        title_score_list.append([])
        for idx2,t in enumerate(taggedsent):
            title_newtag=conv_pos(t[1])
            title_lemmatized=wnl.lemmatize(t[0])

            #Adding Title Word Record
            rev_word=HotelSentiment()
            cnt+=1
            rev_word.seq_no=cnt
            rev_word.reviewID=HotelReview.objects.get(id=df['id'].loc[i])
            rev_word.word=title_lemmatized
            rev_word.type="title"
            rev_word.lemma_word=title_lemmatized
            rev_word.word=t[0]
            rev_word.pos_tag=t[1]
            if(title_newtag!=None):
                synsets = list(swn.senti_synsets(title_lemmatized, title_newtag))
                #score=0
                if(len(synsets)>0):
                    #score=synsets[0].pos_score()-synsets[0].neg_score()

                    rev_word.pos_senti_score=synsets[0].pos_score()
                    rev_word.neg_senti_score=synsets[0].neg_score()
                    rev_word.obj_senti_score=synsets[0].obj_score()
                    #title_score_list[idx].append(synsets[0].pos_score())
                    #title_score_list[idx].append(synsets[0].neg_score())
            rev_word.save()
                    #for syn in synsets:
                    #    score+=syn.pos_score()-syn.neg_score()

                    #score_list[idx].append(score/len(synsets))


    """count=0
    total=0
    for score_sent in score_list:
        for word_score in score_sent:
            total+=word_score
            count+=1
    df['review'].loc[i]=review
    df['Senti_Score'].loc[i]=round(float(total)/count,4)

    print(df['id'].loc[i])
    rev_rec=Review.objects.get(id=df['id'].loc[i])
    rev_rec.review=review
    rev_rec.sentiScore=float(total)/count

    rev_rec.save()
    print(round(float(total)/count,4))"""

"""import matplotlib.pyplot as plt
from matplotlib import use
use('Qt4Agg')

print(df)"""
#plt.scatter(df['rating'], df['Senti_Score'])


#df.boxplot(column="Senti_Score", by="rating")
#plt.show()