import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
import nltk
import boto
import boto3
from boto.sqs.message import Message
import boto.sqs
from textblob import TextBlob
import json


client2 = boto3.client(
    "sns",
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name="us-east-1"
)

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='')

def lambda_handler(event, context):
    while(True):
        try:
            for message in queue.receive_messages(MessageAttributeNames=['All']):
                data=str(message.body)
                print(data)
                #data2=json.loads(data)
                analysis=TextBlob(data)
                polarity=analysis.sentiment.polarity
                print(polarity)
                if polarity == 0:
                    polarity_expression='neutral'
                elif polarity >0:
                    polarity_expression='positive'
                else:
                    polarity_expression='negative'
                print(polarity_expression)
                lat = float(message.message_attributes.get('lat').get('StringValue'))
                print(str(message.message_attributes.get('lat').get('StringValue')))
                lng = float(message.message_attributes.get('lng').get('StringValue'))
                print(str(message.message_attributes.get('lng').get('StringValue')))
                coordinates=[]
                coordinates.append(lat)
                coordinates.append(lng)
                print(coordinates)
                
                m={"content":data,"coordinates":coordinates,"polarity_expression":polarity_expression,"polarity":polarity}
                topic_arn = ''
                client2.publish(TopicArn=topic_arn,
                                Message=json.dumps({'default': json.dumps(m)}),
                                MessageStructure='json')
                print(polarity)
                
                message.delete()
                
        except:
            continue
