import json
import os
import requests
import flickrapi
import webbrowser
import uuid
from joblib import Parallel, delayed

api_key = #your key here
api_secret = #your secret here

def get_latest_xkcd():
    """Get the latest XKCD comic."""
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['img']

def get_previous_xkcd(num):
    """Get the previous XKCD comic."""
    url = 'https://xkcd.com/{}/info.0.json'.format(num)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['img']

def download_xkcd(url):
    """Download the XKCD comic."""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def save_xkcd(comic, filename):
    """Save the XKCD comic."""
    with open(filename, 'wb') as f:
        f.write(comic)

def ConnectFlickr(api_key, api_secret):
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    print('Step 1: authenticate')

    # Only do this if we don't have a valid token already
    if not flickr.token_valid(perms='delete'):

        # Get a request token
        flickr.get_request_token(oauth_callback='oob')

        # Open a browser at the authentication URL. Do this however
        # you want, as long as the user visits that URL.
        authorize_url = flickr.auth_url(perms='delete')
        webbrowser.open_new_tab(authorize_url)

        # Get the verifier code from the user. Do this however you
        # want, as long as the user gives the application the code.
        verifier = str(input('Verifier code: '))

        # Trade the request token for an access token
        flickr.get_access_token(verifier)
    return flickr

def UploadFlickr(flickr, filename, title, description, tags):
    flickr.upload(filename=filename, title=title, description=description, tags=tags)

def fetch_and_upload(i):
    print('getting xkcd {}'.format(i))
    comic = download_xkcd(get_previous_xkcd(i))
    filename = 'xkcd{}.png'.format(i)
    save_xkcd(comic, filename)
    UploadFlickr(flickr, filename, 'xkcd{}'.format(i), 'xkcd{}'.format(i), 'xkcd')

def fetch_range(start, end):
    flickr = ConnectFlickr(api_key, api_secret)
    Parallel(n_jobs=50)(delayed(fetch_and_upload)(i) for i in range(2000, 2664)) # 2664 is the latest xkcd

def fetch_newest():
    flickr = ConnectFlickr(api_key, api_secret)
    print('getting xkcd')
    comic = download_xkcd(get_latest_xkcd())
    filename = 'xkcd{}.png'.format(uuid.uuid4())
    save_xkcd(comic, filename)
    UploadFlickr(flickr, filename, filename.replace(".png",""), filename.replace(".png",""), 'xkcd')
