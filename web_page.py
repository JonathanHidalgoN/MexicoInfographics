import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as py
import asyncio

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


"""
This function displays a counter of the population of Mexico.

Parameters:
        children_per_second (float): The number of children per second.
        population (int): The initial population.

Returns:
        None
"""


async def population_counter(
    t: st._DeltaGenerator = st.empty(),
    children_per_second: float = 0.07,
    population: int = 126e6,
) -> None:
    counter = st.empty()
    current_population = population
    header_text = "Live population"
    digit_template = '<div style="display: inline-block; border: 4px solid black; padding: 5px; margin-right: 5px;">{}</div>'
    st.write(header_text)

    while True:
        current_population += 1

        digits = [digit_template.format(digit) for digit in str(current_population)]

        counter.markdown("".join(digits), unsafe_allow_html=True)

        # time.sleep(children_per_second)
        r = await asyncio.sleep(children_per_second)


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
population, _ = client.get_observation("population")
# TO DO: Maybe this has to be handled in the APIClient class
population = population[0][0]
col1, col2 = st.columns(2)

with col1:
    st.write("## Population")


# Request the data for the population male/female
"""male_female_population_data, male_female_population_dates = client.get_observation("male_female_population")
male_population = male_female_population_data[0]
female_population = male_female_population_data[1]
male_female_population_dates = male_female_population_dates[0]
#Maybe this is not good here
assert(len(male_female_population_dates) == len(male_population) == len(female_population))

st.write("Scatter plot of male population")
fig, ax = plt.subplots()
ax.scatter(male_female_population_dates, male_population)
st.pyplot(fig)
"""

with col2:
    # Can't work with async functions in streamlit, but this hack works
    # just run this at the end of the script and col will keep
    # in the same place
    text = st.empty()
    asyncio.run(
        population_counter(t=text, children_per_second=0.046, population=population)
    )
