import json
import requests
from typing import Dict, Any

class APIClient:

    def __init__(self, api_key : str, api_urls : Dict[str, bool])-> None:
        '''
        This class is used to store the API key and the API urls.
        
        Parameters:
            api_key (str): The API key.
            api_urls (Dict[str, bool]): The API urls.

        Returns:
            None

        '''
        self._api_key = api_key
        self._api_urls = api_urls

    def urls_info(self) -> list[str]:
        '''
        This method returns the info that can be obtained with urls.

        Parameters:
            None

        Returns:
            Dict[str, bool]: The API urls.

        '''
        return self._api_urls.keys()

    def make_request(self, key : str) -> Dict[str, Any]:
        '''
        This method makes the request to the API.

        Parameters:
            key (str): The key to select the url.

        Returns:
            Dict[]: The data obtained from the API.

        '''
        url = self._api_urls[key][0]
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        else:
            return None
        
if __name__ == '__main__' :
    from urls import urls 
    def get_token():
        with open('mex_api.txt') as f:
            token = f.read()
        return token
    token = get_token()
    client = APIClient(token, urls)
    print(client.urls_info())
    population_data = client.make_request('population')
    pass