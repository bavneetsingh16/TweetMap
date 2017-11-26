import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
import nltk
import certifi
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from requests_aws4auth import AWS4Auth
import tweepy
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
import boto3
from multiprocessing import Process
from textblob import TextBlob
from boto.sqs.message import Message

#sqs = boto3.resource('sqs')
#queue = sqs.get_queue_by_name(QueueName='second2.fifo')
access_token = ""
access_secret = ""
consumer_key = ""
consumer_secret = ""

host = 'search-twitterdata-7pjdmgnouvfgjif4lryzj3pgdi.us-east-1.es.amazonaws.com'

aws_id =''
aws_key= ''
auth = AWSRequestsAuth(aws_access_key=aws_id,
                       aws_secret_access_key=aws_key,
                       aws_host=host,
                       aws_region='us-east-1',
                       aws_service='es')

port=443
client = Elasticsearch(
    hosts=[{'host': host,'port':port}],
    ca_certs=certifi.where(),
    use_ssl=True,
    http_auth=auth,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
'''client2 = boto3.client(
    "sns",
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name="us-east-1"
)'''
#topic_arn = 'arn:aws:sns:us-east-1:727407189833:notifications'
#client = Elasticsearch(host={'host': host},ca_certs=certifi.where(),use_ssl=True,verify_certs=True)
class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):
        '''with open('mine2.txt', 'a+') as f:
            f.write(data)'''
        data_json = json.loads(data)
        try:
            coordinates = data_json['place']['bounding_box']['coordinates']
            tweet = json.dumps(data_json['text'])
            place = json.dumps(data_json['place'])

            if place is not None and data_json.get('user').get('lang') == 'en':
                if coordinates[0] is not None and len(coordinates[0]) > 0:
                    lat_x = 0
                    long_y = 0
                    for c in coordinates[0]:
                        lat_x = (lat_x + c[0])
                        long_y = (long_y + c[1])
                    lat_x /= len(coordinates[0])
                    long_y /= len(coordinates[0])
                    coordinates = [lat_x, long_y]
                data_string = str(coordinates) + ","+ str(tweet.encode('utf-8')) + "\n"
                #print data_string
                analysis=TextBlob(tweet)
                polarity=analysis.sentiment.polarity
                print(polarity)
                if polarity == 0:
                    polarity_expression='neutral'
                elif polarity >0:
                    polarity_expression='positive'
                else:
                    polarity_expression='negative'
                #m=Message()
                m={"content": tweet,"coordinates": coordinates,"polarity_expression":polarity_expression,"polarity":polarity}
                # for local purpose storing in a file
                '''with open('mine1.txt', 'a') as f:
                    f.write(data_string)'''
                '''m.message_attributes={
                      "tweets": {
                        "DataType": "String",
                        "StringValue": tweet
                       },
                      "lat": {
                        "DataType": "String",
                        "StringValue": str(coordinates[0])
                       },
                      "lng": {
                        "DataType": "String",
                        "StringValue": str(coordinates[1])
                       }
                }'''
                   
                try:
        
                    #m.MessageGroupId='messageGroup3'
                    
                    #queue.send_message(MessageAttributes=m.message_attributes,MessageBody=tweet,
                        #MessageGroupId=m.MessageGroupId)
                    client.index(index='cloud_tweet1', doc_type='twitter', body=m)
                    #queue.send_message(
                      #      MessageBody=str(m),
                      #      MessageGroupId='messageGroup1'
                      #      )
                    
                    #client2.publish(Message=str(m), TopicArn=topic_arn)
                    #retreivesqs()
                except:
                    print('ElasticSearch indexing failed')
                    
        except (KeyError, TypeError):
            pass
        return True

    def on_error(self, status):
        print (status)
        
"""def retreivesqs():
    while(True):
        try:
            for message in queue.receive_messages():
                with open('mine5.txt', 'a') as f:
                    f.write(message.body)
                message.delete()
        except:
            continue"""
'''def print2(b):
    with open("multitext7.txt","a+")as f:
        f.write(str(b))
    while(True):
        try:
            for message in queue.receive_messages():
                with open('mine5.txt', 'a') as f:
                    f.write(message.body)
                message.delete()
        except:
            continue'''
        
    
def lambda_handler():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, StdOutListener())
    stream.filter(track=['music', 'movies', 'games','google','trump','modi','football','united states','india','hollywood'])
    #p1 = Process(target = stream.filter(track=['music', 'movies', 'games','google','trump','modi','football','united states','india','hollywood']))
    #p1 = Process(target = print2())
    #p1.start()
    #p1.join(Process(target = print2(3)))
    #p1.start()
if __name__ == '__main__':
    lambda_handler()
