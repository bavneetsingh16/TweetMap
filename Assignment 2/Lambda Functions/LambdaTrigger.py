from __future__ import print_function

import json
import certifi
from requests_aws4auth import AWS4Auth
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests

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
    message =json.dumps(event['Records'][0]['Sns']['Message'])
    print("From SNS: " + message)
    msg=json.loads(message)
    client.index(index='cloud_tweet1', doc_type='twitter', body=msg)
    return message