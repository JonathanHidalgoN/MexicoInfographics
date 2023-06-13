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

    @staticmethod
    def _format_url(url : str, api_key : str) -> str:
        '''
        This method formats the url to make the request.

        Parameters:
            url (str): The url to format.
            api_key (str): The API key.

        Returns:
            str: The formatted url.
        '''
        target_string = '[Aquí va tu Token]'
        return url.replace(target_string, api_key)

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
        formated_url = self._format_url(url, self._api_key)
        response = requests.get(formated_url)
        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        else:
            raise Exception('The request failed.')
        
    def get_observation(self, key : str) -> dict[int, list[float]]:
        '''
        This method returns the observation values.

        Parameters:
            key (str): The key to select the url.

        Returns:
            dict[int, list[float]]: The observation values.

        '''
        data = self.make_request(key)
        num_series = len(data['Series'])
        observations = {idx : [] for idx in range(num_series)}
        for idx,serie in enumerate(data['Series']):
            for obs in serie['OBSERVATIONS']:
                observations[idx].append(float(obs['OBS_VALUE']))
        return observations
    
        
if __name__ == '__main__' :
    from urls import urls 
    def get_token():
        with open('mex_api.txt') as f:
            token = f.read()
        return token
    token = get_token()
    client = APIClient(token, urls)
    print(client.urls_info())
    population = client.get_observation('population')
    male_female_population = client.get_observation("male_female_population")
    pass