import json
import os
import requests

url = 'https://westmd.craigslist.org/search/sss'

search_params = {
    'sort' : 'rel',
    'min_price' : '50',
    'query' : 'bobcat',
    'srchType' : 'T'
}

response = requests.get(url, params=search_params)

json_response = json.dumps(response.text)   
print(json_response)
#print(response.url)
#print(response.headers)