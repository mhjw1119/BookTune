# 알라딘 API로 DB 구축하기.

import requests
from django.shortcuts import render
from decouple import config
import requests

ALADIN_API_URL = config('ALADIN_API_URL')
ALADIN_API_KEY = config('ALADIN_API_KEY')


params = {
    'ttbkey': ALADIN_API_KEY,
    'QueryType': 'ItemNewAll',
    'MaxResults': '50',
    'start': '1',
    'SearchTarget': 'Book',
    'output': 'js',
    'Version': '20131101'
}

response = requests.get(ALADIN_API_URL, params=params).json()

result = []
for item in response['item']:
    info = {
        'isbn': item['isbn'],
        'title': item['title'],
        'pubDate': item['pubDate'],
        'publisher': item['publisher'],
        'author': item['author'],
        'description': item['description'],
        'cover': item['cover'],
        'customerReviewRank': item['customerReviewRank']
    }
    result.append(info)


print(result)

