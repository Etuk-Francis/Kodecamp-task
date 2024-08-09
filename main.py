#all the code pertaining to project 1 /v1/forecast

#url = 'https://api.open-meteo.com/v1/forecast'

# API -> URL (endpoint) -> http request -> (optional parameters) -> specific json response
long = 45.3
lat = 456.3

import requests

url = f'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41'

data = requests.get(url)  

print(data)

result = data.json()
print(result)

long = result['longitude']
print(long)