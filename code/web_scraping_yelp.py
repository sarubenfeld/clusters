#import yelp.search as yelp
import yelp
import yelp_helpers
from pymongo import MongoClient
from pymongo import errors
from bs4 import BeautifulSoup
import requests
import time
import pdb
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

'''
Using Yelp's python client:

https://github.com/Yelp/yelp-api/tree/master/v2/python

'''

mongoclient = MongoClient()
db = mongoclient.yelp
coll = db.restaurants

def authorize():

    auth = Oauth1Authenticator(
        consumer_key="",
        consumer_secret="",
        token="",
        token_secret=""
    )
    client = Client(auth)
    return client

def make_response(client, url_params):
    response = client.search(**url_params)

    return response

# def make_request(params):
#     return yelp.request(params, key, c_secret, token, t_secret)

def insert_business(busi, collection):
        if not collection.find_one({"id" : busi['id']}):
            try:
                print "Inserting restaurant " + str(busi['name'].encode('ascii', 'ignore'))
                collection.insert(busi)
            except errors.DuplicateKeyError:
                print "Duplicates"
        else:
            print "In collection already"

def make_clean_business_dict(business):
    business_dict = business.__dict__
    business_dict['location'] = business_dict['location'].__dict__
    business_dict['location']['coordinate'] = business_dict['location']['coordinate'].__dict__
    for bad_field in ['gift_certificates', 'eat24_url', 'reservation_url', 'deals']:
        del business_dict[bad_field]
    return business_dict

def get_meta(collection):


    client = authorize()

    url_params = {'location': 'san francisco', 'category_filter':'restaurants'}

    url_params['limit'] = 20
    url_params['offset'] = 0

    total_num = make_response(client, url_params).total
    total_results = collection.find().count()

    while total_results < total_num and url_params['offset'] < total_num:
        response = make_response(client, url_params)

        for business in response.businesses:
            business_dict = make_clean_business_dict(business)
            insert_business(business_dict, collection)

        url_params['offset'] += 20
        time.sleep(1)

if __name__ == '__main__':
    get_meta(coll)
