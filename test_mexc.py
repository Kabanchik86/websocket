import requests

def make_request(endpoint, params=None):
    base_url = 'https://api.mexc.com'
    response = requests.get(base_url + endpoint, params=params)
    result = response.json()
    return result

if __name__ == '__main__':
    endpoint = '/api/v3/depth'
    params = {'symbol':'BTCUSDT'}
    response = make_request(endpoint, params)
    print(response)