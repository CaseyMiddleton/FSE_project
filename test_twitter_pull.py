from twitter_pull import *
import json

def test_auth():
    ''' Test if authorization function returns a string '''
    token = auth()
    assert(type(token) is str)

def test_write_query():
    ''' Test that write query function returns a string '''
    query = write_query("hello") # query with one parameter
    assert(query == "hello lang:en -is:retweet")
    query = write_query("hello","goodbye","AND") # query with two parameters
    assert(query == "hello goodbye lang:en -is:retweet")

def test_connect_to_endpoint():
    ''' Test if the appropriate response code (200) is received from the endpoint '''
    bearer_token = auth()
    headers = create_headers(bearer_token)
    keyword = write_query("covid")
    max_results = 100
    url = create_url(keyword, max_results)
    json_response = connect_to_endpoint(url[0], headers, url[1])
    assert(type(json.dumps(json_response)) is str)
