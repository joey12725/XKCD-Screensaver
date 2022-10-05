from xkcd import ConnectFlickr

api_key = input('API key: ')
api_secret = input('API secret: ')
oldest = input('Oldest comic number: ')
newest = input('Newest comic number: ')
fetch_range(oldest, newest)