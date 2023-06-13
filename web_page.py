import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as py
import time

from urls import urls
from APIClient import APIClient


def get_token(path: str = "mex_api.txt") -> str:

    """
    This function returns the token to make the request to the API.

    Parameters:
        path (str): The path of the file that contains the token.

    Returns:
        str: The token.
    """
    with open(path) as f:
        token = f.read()
    return token


# TO DO: Check how to use the image for github
map_image_path = "mex_map.jpg"

st.title("Mexico population infographic")
st.write(
    "Mexico (Spanish: México), officially the United Mexican States, is a country in the southern portion of North America. "
    "It is bordered to the north by the United States; to the south and west by the Pacific Ocean; to the southeast by Guatemala"
    ", Belize, and the Caribbean Sea; and to the east by the Gulf of Mexico."
)
st.image(map_image_path, caption="Map of Mexico", use_column_width=True)
st.write(
    "We will use the API of the National Institute of Statistics and Geography (INEGI) to obtain the information displayed in this page."
)

# Instantiate the APIClient class
token = get_token()
client = APIClient(token, urls)

# Get the population data
population = client.get_observation("population")[0][0]

st.write("## Population")

def population_counter(target_population : int = population, sleep_time : float = 0.05, increment : int = 1000, start : int = 1e8):
    counter = st.empty()
    current_population = start
    while current_population < target_population:
        current_population += increment  # Adjust the increment as desired
        counter.markdown(
            f'<h1 style="font-size: 72px;">{current_population}</h1>',
            unsafe_allow_html=True
        )
        time.sleep(sleep_time)  # Adjust the sleep duration to control the speed of the counter

    counter.markdown(
        f'<h1 style="font-size: 72px;">{target_population}</h1>',
        unsafe_allow_html=True
    )

population_counter()