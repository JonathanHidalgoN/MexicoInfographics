import json
import requests
from typing import Dict, Any, Tuple, Iterable


class APIClient:
    def __init__(self, api_key: str, api_urls: Dict[str, bool]) -> None:
        """
        This class is used to store the API key and the API urls.

        Parameters:
            api_key (str): The API key.
            api_urls (Dict[str, bool]): The API urls.

        Returns:
            None

        """
        self._api_key = api_key
        self._api_urls = api_urls

    @staticmethod
    def _format_url(url: str, api_key: str) -> str:
        """
        This method formats the url to make the request.

        Parameters:
            url (str): The url to format.
            api_key (str): The API key.

        Returns:
            str: The formatted url.
        """
        target_string = "[Aquí va tu Token]"
        return url.replace(target_string, api_key)

    def urls_info(self) -> list[str]:
        """
        This method returns the info that can be obtained with urls.

        Parameters:
            None

        Returns:
            Dict[str, bool]: The API urls.

        """
        return self._api_urls.keys()

    def make_request(self, key: str) -> Dict[str, Any]:
        """
        This method makes the request to the API.

        Parameters:
            key (str): The key to select the url.

        Returns:
            Dict[]: The data obtained from the API.

        """
        url = self._api_urls[key][0]
        formated_url = self._format_url(url, self._api_key)
        response = requests.get(formated_url)
        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        else:
            raise Exception("The request failed.")

    def get_observation(
        self,
        key: str,
        obs_keys: Iterable[Any] = None,
    ) -> Tuple[Dict[int, list[float]], Dict[int, list[str]]]:
        """
        This method returns the observation values and dates.

        Parameters:
            key (str): The key to select the url.
            obs_keys (Iterable[Any]): The keys to select the observations.

        Returns:
            Tuple(Dict[Iterable[Any], list[float]], Dict[Iterable[Any], list[str]]):
            The observation values and dates for each observation.
        """
        data = self.make_request(key)
        num_series = len(data["Series"])
        if obs_keys is None:
            obs_keys = [f"{i}" for i in range(num_series)]
        observations = {idx: [] for idx in obs_keys}
        dates = {idx: [] for idx in obs_keys}
        for idx, serie in zip(obs_keys, data["Series"]):
            for obs in serie["OBSERVATIONS"]:
                observations[idx].append(float(obs["OBS_VALUE"]))
                dates[idx].append(obs["TIME_PERIOD"])
        return observations, dates


if __name__ == "__main__":
    from urls import urls

    def get_token():
        with open("mex_api.txt") as f:
            token = f.read()
        return token

    token = get_token()
    client = APIClient(token, urls)
    print(client.urls_info())
    population, date1 = client.get_observation("population")
    male_female_population, date = client.get_observation(
        "50-54/55-59/60-64/65-69/70-74/male_female_population"
    )
    pass
