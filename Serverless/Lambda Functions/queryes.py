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

access_token = ""
access_secret = ""
consumer_key = ""
consumer_secret = ""

host = ''

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

def lambda_handler(event, context):
  name3=str(event['params']['querystring']['options'])
  result=client.search(index="cloud_tweet1", body={"size":10000,"query": {"match": {"content": name3}}})
  location = [dict() for num in range(len(result['hits']['hits']))]
  for pos in range(len(result['hits']['hits'])):
      jsonvalues = result['hits']['hits'][pos]['_source']
      temp = str(jsonvalues['coordinates']).strip('[').strip(']').split(',')
      location[pos] = dict(lng=float(temp[0]), lat=float(temp[1]),sent=str(jsonvalues['polarity_expression']),data=str(jsonvalues['content']))
  return location
  


  