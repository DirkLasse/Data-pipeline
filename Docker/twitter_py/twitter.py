from pydoc import cli
import tweepy
from credentials import BEARER_TOKEN
import logging
import pymongo

mongo = pymongo.MongoClient(host="mongodb", port=27017)
if mongo:
     logging.critical(f"\nmongo DB conected {mongo}")
else:
    logging.critical(f'\nConecting mongoDB failed{mongo}')   
mongo.drop_database('my_db')
db = mongo.my_db
dbcoll = db.my_collection

client = tweepy.Client(bearer_token=BEARER_TOKEN)
if client:
    logging.critical("\nTwitter Authentication OK")
else:
    logging.critical('\nVerify your Twitter credentials')
    
'''
Kate Jarmul         @kjam           ethical AI activist
Allen Downey        @AllenDowney    probabilities
Sebastian Raschka   @rasbt          deep learning
Kate Compton        @GalaxyKate     generative artist
Andreas Müller      @amuellerml     sklearn
Julia Evans         @b0rk           linux, networking
Ines Montani        @_inesmontani   spacy, NLP
Jake VanderPlas     @jakevdp        data visualization
Wes McKinney        @wesmckinn      pandas
Andrew Ng           @AndrewYNg      deep learning guru
'''
account = client.get_user(username='kjam', user_fields=['name', 'id', 'created_at'])
user = account.data
tweets = client.get_users_tweets(id=user.id, tweet_fields=['id', 'text', 'created_at',
                                                           'attachments','entities','geo',
                                                          'in_reply_to_user_id','lang',
                                                          'possibly_sensitive','referenced_tweets','source',
                                                          'public_metrics','withheld','author_id'],max_results=100)
if tweets:
    logging.critical(f"Actual Tweets from {user.name} are downloaded!")
else:
    logging.critical(f"Actual Tweets from {user.name} FAILED downloading!")

for tweet in tweets.data:
    #print(dict(tweet))
    try:
        dbcoll.insert_one(dict(tweet))
        logging.critical(f"Wrote tweet in mongo DB")
    except:
        logging.critical(f"Error insert tweet in mongo DB")