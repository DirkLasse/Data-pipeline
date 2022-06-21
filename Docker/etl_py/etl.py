from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import pymongo
import logging
from sqlalchemy import text, create_engine, inspect
from credentials import PASSWORD
import re
from time import sleep

def clean_tweets(tweet):
    mentions_regex= '@[A-Za-z0-9]+'  # "+" means one or more times
    url_regex='https?:\/\/\S+' # this will catch most URLs; "?" means 0 or 1 time; "S" is anything but whitespace
    hashtag_regex= '#'
    rt_regex= 'RT\s'
    tweet = re.sub(mentions_regex, '', tweet)  # removes @mentions
    tweet = re.sub(hashtag_regex, '', tweet) # removes hashtag symbol
    tweet = re.sub(rt_regex, '', tweet) # removes RT to announce retweet
    tweet = re.sub(url_regex, '', tweet) # removes most URLs
    return tweet

sleep(10)
HOST = 'mypg'
USERNAME = 'postgres'
PORT = '5432'
DB = 'postgres'
conn_string = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'

engine = create_engine(conn_string,echo=True)

if engine:
     logging.critical(f"\npsql conected to ETL {engine}")
else:
    logging.critical(f'\nConecting psql ETL failed{engine}')  

#engine.execution_options(isolation_level="AUTOCOMMIT").execute('DROP DATABASE IF EXISTS ' + DB+";")

#try: 
#    engine.execution_options(isolation_level="AUTOCOMMIT").execute('CREATE DATABASE ' + DB+";")
#except Exception as db_exc:
#    logging.exception("Exception creating database: faild" ) 
#engine.execution_options(isolation_level="AUTOCOMMIT").execute('\c ' + DB)


analyser = SentimentIntensityAnalyzer()

mongo = pymongo.MongoClient(host="mongodb", port=27017)
if mongo:
     logging.critical(f"\nmongo DB conected to ETL {mongo}")
else:
    logging.critical(f'\nConecting mongoDB to ETL failed{mongo}')   

db = mongo.my_db
if db is not None:
     logging.critical(f"\nmongo DB conected my_db {db}")
else:
    logging.critical(f'\nConecting mongoDB to my_db failed{db}')  
dbcoll = db.my_collection
if dbcoll is not None:
     logging.critical(f"\nmongo DB conected collection {dbcoll}")
else:
    logging.critical(f'\nConecting mongoDB to collection failed{dbcoll}') 

df=pd.DataFrame(list(dbcoll.find()))
logging.critical(f'\n DF from mongo {df.columns}')
df_metric=pd.DataFrame(list(df["public_metrics"]))
df[df_metric.columns]=df_metric
df.drop(["_id","public_metrics","entities","referenced_tweets","attachments"],axis=1,inplace=True)
df["text"] = df["text"].apply(clean_tweets)
pol_scores = df['text'].apply(analyser.polarity_scores).apply(pd.Series)
df[pol_scores.columns]=pol_scores

df.to_sql('tweets', engine,if_exists='replace')
