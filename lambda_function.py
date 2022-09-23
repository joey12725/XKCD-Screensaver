import json
from xkcd import fetch_newest

def lambda_handler(event, context):
    fetch_newest()
    return {
        'statusCode': 200,
        'body': 'Fetched newest xkcd'
    }

#lambda_handler(None, None)