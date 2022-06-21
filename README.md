# A Data Pipline with Docker and sentiment Analysis on tweets

- Extract tweets with [Tweepy API](https://docs.tweepy.org/en/stable/index.html)and  load them in MongoDB **twitter_py**
- Extract the tweets from MongoDB, perform sentiment analyisis on the tweets and load the transformed data in a PostgresDB with **etl_py**

## Usage
- Install [Docker](https://docs.docker.com/get-docker/) on your machine
- Clone the repository: ```git clone https://github.com/DirkLasse/Data-pipeline.git```
- Get credentials for Twitter API and insert them in ```twitter_py/credentials.py``` with ```BEARER_TOKEN= XXXXX```
- Go into toe Docker folder
- Run ```docker-compose build```, then ```docker-compose up``` in terminal
- Open the Matabase docker in the webbrowser with ```http://localhost:3000/```
- in step 3 use 
  * Display name: tweets
  * Host: mypg 
  * Database name: postgres
  * Username: postgres
  * Password: postgres
- now querys can be create on the tweets with sentiment analysis