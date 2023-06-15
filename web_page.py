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


async def population_counter(
    t: st._DeltaGenerator = st.empty(),
    children_per_second: float = 0.07,
    population: int = 126e6,
) -> None:
    # This function displays a counter of the population of Mexico.

    # Parameters:
    #        children_per_second (float): The number of children per second.
    #        population (int): The initial population.

    # Returns:
    #        None

    current_population = population
    header_text = "Live population"
    digit_template = '<div style="display: inline-block; border: 4px solid black; padding: 5px; margin-right: 5px;">{}</div>'
    st.write(header_text)

    while True:
        current_population += 1

        digits = [digit_template.format(digit) for digit in str(current_population)]

        t.markdown("".join(digits), unsafe_allow_html=True)

        # time.sleep(children_per_second)
        r = await asyncio.sleep(children_per_second)


def make_population_distribution_plot(c_APIclient) -> None:
    """
    This function makes a plot of the population distribution in Mexico.
    Parameters:
        c_APIclient (APIClient): The APIClient object.
    Returns:
        None

    Raises:
        assertion error if population data and dates are not the same length.
    """
    (
        male_female_population_data,
        male_female_population_dates,
    ) = c_APIclient.get_observation("male_female_population")
    male_population = male_female_population_data["0"]
    female_population = male_female_population_data["1"]
    male_female_population_dates = male_female_population_dates["0"]
    assert (
        len(male_female_population_dates)
        == len(male_population)
        == len(female_population)
    )
    sns.set(style="darkgrid")
    plt.rcParams["axes.facecolor"] = "black"
    fig, ax = plt.subplots(facecolor="black")
    ax.scatter(male_female_population_dates, male_population, label="Male Population")
    ax.scatter(
        male_female_population_dates, female_population, label="Female Population"
    )
    ax.set_xlabel("Date", color="white")
    ax.set_ylabel("Population", color="white")
    ax.set_title("Population Distribution", color="white")
    legend = ax.legend(
        facecolor="black", edgecolor="white", fontsize="small", framealpha=1
    )
    for text in legend.get_texts():
        text.set_color("white")
    ax.set_xticklabels(male_female_population_dates, rotation=45)
    ax.tick_params(colors="white")
    st.pyplot(fig)


def unfold_population_per_age_request(key: str, api_client, labels: list[str]) -> tuple:
    """
    This function unfolds the population per age request.
    Parameters:
        key (str): The key of the request.
        api_client (APIClient): The APIClient object.
        labels (list[str]): The labels of the data.
    Returns:
        tuple: A tuple with the data and the dates.
    Raises:
        assertion error if population data and dates are not the same length or dates list is not equal.
    """

    d_population, dates = api_client.get_observation(key, labels)
    n_sets = len(d_population)
    # Assert all dates and len of data are the same
    # is this necessary? or expensive?
    # I think it its because, this checks:
    # 1. All dates are the same
    # 2. All data has the same length
    all(dates[labels[0]] == dates[label] for label in labels)
    return d_population, dates[labels[0]]


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
population = population["0"][0]
col1, col2 = st.columns(2)

with col1:
    st.write("## Population")

st.write(
    "With a population of over 126 million, it is the 10th-most-populous country and has the most Spanish speakers."
    " Mexico is organized as a federal republic comprising 31 states and Mexico City, its capital."
)

make_population_distribution_plot(client)

population_age_keys = [
    "0-4/5-9/10-14/15-19/20-24/male_female_population",
    "25-29/30-34/35-39/40-44/45-49/male_female_population",
    "50-54/55-59/60-64/65-69/70-74/male_female_population",
]

population_age_labels_1 = [f"{i}-{i+4}" for i in range(0, 25, 5)]
population_age_labels_2 = [f"{i}-{i+4}" for i in range(25, 50, 5)]
population_age_labels_3 = [f"{i}-{i+4}" for i in range(50, 75, 5)]

population_age_1, date = unfold_population_per_age_request(
    population_age_keys[0], client, population_age_labels_1
)
population_age_2, _ = unfold_population_per_age_request(
    population_age_keys[1], client, population_age_labels_2
)
population_age_3, _ = unfold_population_per_age_request(
    population_age_keys[2], client, population_age_labels_3
)

population_age = {**population_age_1, **population_age_2}
population_age = {**population_age, **population_age_3}

dataframe = pd.DataFrame(population_age, index=date)
st.dataframe(dataframe)


with col2:
    # Async do not work with streamlit, put this in the end of the script,
    # the col will keep in the same place
    t = st.empty()
    asyncio.run(
        population_counter(t=t, children_per_second=0.046, population=population)
    )
