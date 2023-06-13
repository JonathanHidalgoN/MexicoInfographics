import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as py

from urls import urls
from APIClient import APIClient

def get_token(path : str = 'mex_api.txt') -> str:

    '''
    This function returns the token to make the request to the API.
    
    Parameters:
        path (str): The path of the file that contains the token.
    
    Returns:
        str: The token.
    '''
    with open(path) as f:
        token = f.read()
    return token
