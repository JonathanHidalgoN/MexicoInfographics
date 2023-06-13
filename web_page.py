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


def population_counter(
    children_per_second: float = 0.07, population: int = 126e6
) -> None:
    """
    This function displays a counter of the population of Mexico.

    Parameters:
        children_per_second (float): The number of children per second.
        population (int): The initial population.

    Returns:
        None
    """

    counter = st.empty()
    current_population = population
    header_text = "Live population"
    digit_template = '<div style="display: inline-block; border: 4px solid black; padding: 5px; margin-right: 5px;">{}</div>'
    st.write(header_text)

    while True:
        current_population += 1  # Adjust the increment as desired

        digits = [digit_template.format(digit) for digit in str(current_population)]

        counter.markdown("".join(digits), unsafe_allow_html=True)

        time.sleep(
            children_per_second
        )  # Adjust the sleep duration to control the speed of the counter


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
col1, col2 = st.columns(2)

with col1:
    st.write("## Population")

with col2:
    population_counter(children_per_second=0.07, population=population)
