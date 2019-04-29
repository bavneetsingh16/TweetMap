from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django import template
from django.template import *
#import twitter_streaming as ts
#import retreive as ret
import json
import requests
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

#host='https://search-twitterdata-7pjdmgnouvfgjif4lryzj3pgdi.us-east-1.es.amazonaws.com/twitter/_search'

def index(request):
	if request.method == 'GET':
		return render(request,'form.html')
    
	if request.method == 'POST':
         name2 = request.POST['options']
         
         name3=str(name2)
         g = json.dumps({
         'size': 1000,
                "query": {
                    "match": {
                        "content": name3
                    }
                }
            })
            
         result = requests.get('https://search-twitterdata-7pjdmgnouvfgjif4lryzj3pgdi.us-east-1.es.amazonaws.com/cloud_tweet1/_search', data=g)
         results = json.loads(result.text)
         location = [dict() for num in range(len(results['hits']['hits']))]
         for pos in range(len(results['hits']['hits'])):
               jsonvalues = results['hits']['hits'][pos]['_source']
               temp = str(jsonvalues['coordinates']).strip('[').strip(']').split(',')
               location[pos] = dict(lng=float(temp[0]), lat=float(temp[1]))
         return render(request,"map2.html",{'lats':location})
