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

#TO DO: Check how to use the image for github
map_image_path = 'mex_map.jpg'

st.title('Mexico population infographic')
st.write('This is a simple and interactive web app that shows the population of Mexico in the last years.')

