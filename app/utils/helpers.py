from streamlit import secrets
from requests import get


def extract_state_names(data):
    """
    This function extracts the state names from the data.
    Parameters:
        data (list): The data.
    Returns:
        list: The state names.
    """
    state = []
    for item in data["features"]:
        state.append(item["properties"]["name"])
    return state


def get_token(path: str = "mex_api.txt") -> str:

    """
    This function returns the token to make the request to the API.

    Parameters:
        path (str): The path of the file that contains the token.

    Returns:
        str: The token.
    """
    try:
        with open(path) as f:
            token = f.read()
    except FileNotFoundError:
        token = secrets["mex_api_token"]
    return token


def create_population_age_labels_sex(start: int, stop: int, step: int) -> list[str]:
    """
    This function creates the labels for the population per age request.
    Parameters:
        start (int): The start age.
        stop (int): The stop age.
        step (int): The step age.
    Returns:
        list[str]: The labels for sthe population per age request.
    """
    labels = []
    for i in range(start, stop, step):
        labels.append(f"{i}-{i+4} male")
        labels.append(f"{i}-{i+4} female")
    return labels


def request_mexico_graph_info():
    """
    This function requests the information to create the graph of Mexico.
    Returns:
        dict: The information to create the graph of Mexico.
    Raises:
        Exception: If the request to the API fails.
    """
    url = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
    try:
        mx_mexico_regions = get(url).json()
    except Exception as e:
        raise e
    if mx_mexico_regions is None:
        raise Exception("The request to the API failed.")
    return mx_mexico_regions
