from streamlit import secrets


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
