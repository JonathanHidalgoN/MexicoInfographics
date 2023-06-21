import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import asyncio


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
    #        t (st._DeltaGenerator): The DeltaGenerator object.
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

    population_df = pd.DataFrame(
        {
            "Date": male_female_population_dates,
            "Male": male_population,
            "Female": female_population,
        }
    )

    fig = px.scatter(
        population_df,
        x="Date",
        y=["Male", "Female"],
        labels={"value": "Population", "variable": "Gender"},
        title="Population Distribution",
    )

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        legend=dict(bgcolor="black", bordercolor="white", font=dict(color="white")),
        xaxis=dict(tickfont=dict(color="white"), tickangle=45),
        yaxis=dict(tickfont=dict(color="white")),
    )

    st.plotly_chart(fig)


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
    # Assert all dates and len of data are the same
    # is this necessary? or expensive?
    # I think it its because, this checks:
    # 1. All dates are the same
    # 2. All data has the same length
    # So, I think it is necessary to avoid errors, but maybe it is expensive
    all(dates[labels[0]] == dates[label] for label in labels)
    return d_population, dates[labels[0]]


def create_age_data_frame() -> pd.DataFrame:
    """
    This function creates a dataframe with the population per age.
    Parameters:
        None
    Returns:
        dataframe: The dataframe with the population per age.
    """
    population_age_1, date = unfold_population_per_age_request(
        web_variables["population_age_keys"][0],
        client,
        web_variables["population_age_labels_1"],
    )
    population_age_2, _ = unfold_population_per_age_request(
        web_variables["population_age_keys"][1],
        client,
        web_variables["population_age_labels_2"],
    )
    population_age_3, _ = unfold_population_per_age_request(
        web_variables["population_age_keys"][2],
        client,
        web_variables["population_age_labels_3"],
    )

    population_age = {**population_age_1, **population_age_2, **population_age_3}
    dataframe = pd.DataFrame(population_age, index=date)
    return dataframe


def add_age_data_frame(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    This funcition merge age columns in the dataframe.
    Parameters:
        dataframe (dataframe): The dataframe to merge.
    Returns:
        dataframe: The dataframe with the merged columns.
    """
    #TODO: This function may be slow, try to optimize it
    col_names = dataframe.columns
    new_col_names = []
    for idx, col_name in enumerate(col_names):
        if idx % 2 == 0:
            tmp = col_name.split(" ")
            new_col_names.append(tmp[0] + " years")
        for idx, col_name in enumerate(col_names):
            if idx % 2 != 0:
                dataframe[new_col_names[idx // 2]] = (
                    dataframe[col_name] + dataframe[col_names[idx - 1]]
                )
        for idx, col_name in enumerate(col_names):
            dataframe.drop(col_name, axis=1, inplace=True)
        return dataframe


def cut_age_dataframe(
    start_year: int,
    end_year: int,
    start_age: str,
    end_age: str,
    original_df: pd.DataFrame,
    filter: str,
) -> pd.DataFrame:
    """
    This function cuts the age dataframe to the specified years and age.
    Parameters:
        start_year (int): The start year.
        end_year (int): The end year.
        start_age (str): The start age.
        end_age (str): The end age.
        original_df (dataframe): The original dataframe.
        fitler (str): The filter to apply to the dataframe.
    Returns:
        dataframe: The dataframe with the specified years and age.
    """
    e_start_age = start_age + " male"
    e_end_age = end_age + " female"
    selected_data_frame = original_df.loc[str(start_year) : str(end_year)].loc[
        :, e_start_age:e_end_age
    ]
    if filter == "Sex":
        return selected_data_frame
    else:
        return add_age_data_frame(selected_data_frame)


def plot_cut_age_dataframe(cut_dataframe: pd.DataFrame) -> None:
    """
    This function plots the cut age dataframe.
    Parameters:
        cut_dataframe (dataframe): The cut dataframe.
    Returns:
        None
    """
    fig = px.line(cut_dataframe)
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Population",
        legend_title="Age",
    )
    st.plotly_chart(fig)


def create_population_age_labels_sex(start: int, stop: int, step: int) -> list[str]:
    """
    This function creates the labels for the population per age request.
    Parameters:
        start (int): The start age.
        stop (int): The stop age.
        step (int): The step age.
    Returns:
        list[str]: The labels for the population per age request.
    """
    labels = []
    for i in range(start, stop, step):
        labels.append(f"{i}-{i+4} male")
        labels.append(f"{i}-{i+4} female")
    return labels


if __name__ == "__main__":

    from urls import urls
    from APIClient import APIClient

    ################################################################################
    #                                WEB VARIABLES                                 #
    web_variables = {
        "map_image_path": "mex_map.jpg",
        "token": get_token(),
        "population_age_labels_1": create_population_age_labels_sex(0, 25, 5),
        "population_age_labels_2": create_population_age_labels_sex(25, 50, 5),
        "population_age_labels_3": create_population_age_labels_sex(50, 75, 5),
        "population_age_range": [f"{i}-{i+4}" for i in range(0, 75, 5)],
        "population_age_keys": [
            "0-4/5-9/10-14/15-19/20-24/male_female_population",
            "25-29/30-34/35-39/40-44/45-49/male_female_population",
            "50-54/55-59/60-64/65-69/70-74/male_female_population",
        ],
        "population_age_years": [year for year in range(1990, 2025, 5)],
    }
    client = APIClient(web_variables["token"], urls)
    population, _ = client.get_observation("population")
    population = population["0"][0]
    age_male_female_dataframe = create_age_data_frame()
    population_age_labels = (
        web_variables["population_age_labels_1"]
        + web_variables["population_age_labels_2"]
        + web_variables["population_age_labels_3"]
    )
    ################################################################################
    ################################################################################
    #                                WEB STRUCTURE                                 #

    st.title("Mexico population infographic")
    st.write(
        "Mexico (Spanish: México), officially the United Mexican States, is a country in the southern portion of North America. "
        "It is bordered to the north by the United States; to the south and west by the Pacific Ocean; to the southeast by Guatemala"
        ", Belize, and the Caribbean Sea; and to the east by the Gulf of Mexico."
    )

    st.image(
        web_variables["map_image_path"], caption="Map of Mexico", use_column_width=True
    )
    st.write(
        "We will use the API of the National Institute of Statistics and Geography (INEGI) to obtain the information displayed in this page."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.write("## Population")

    st.write(
        "With a population of over 126 million, it is the 10th-most-populous country and has the most Spanish speakers."
        " Mexico is organized as a federal republic comprising 31 states and Mexico City, its capital."
    )

    make_population_distribution_plot(client)

    col3, col4 = st.columns(2)
    with col3:
        st.write("### Year categories")
        start_year = st.selectbox(
            "Start year", web_variables["population_age_years"], index=0
        )
        end_year = st.selectbox(
            "End year",
            web_variables["population_age_years"],
            index=web_variables["population_age_years"].index(2020),
        )
    with col4:
        st.write("### Age categories")
        start_age = st.selectbox(
            "Start age", web_variables["population_age_range"], index=0
        )
        end_age = st.selectbox(
            "End age",
            web_variables["population_age_range"],
            index=web_variables["population_age_range"].index("70-74"),
        )

    col5, col6 = st.columns(2)
    with col5:
        st.write("## Population per age")
    with col6:
        age_population_filter = st.selectbox("Filter", ["None", "Sex"], index=0)
    # TO DO : Add error handling for the case when the start year is greater than the end year
    if age_population_filter == "Sex":
        selected_age_data_frame = cut_age_dataframe(
            start_year,
            end_year,
            start_age,
            end_age,
            age_male_female_dataframe,
            filter=age_population_filter,
        )
        st.dataframe(selected_age_data_frame)
        plot_cut_age_dataframe(selected_age_data_frame)
    else:
        selected_age_data_frame = cut_age_dataframe(
            start_year,
            end_year,
            start_age,
            end_age,
            age_male_female_dataframe,
            filter=age_population_filter,
        )
        st.dataframe(selected_age_data_frame)
        plot_cut_age_dataframe(selected_age_data_frame)
    with col2:
        # Async do not work with streamlit, put this in the end of the script,
        # the col will keep in the same place
        t = st.empty()
        asyncio.run(
            population_counter(t=t, children_per_second=21, population=population)
        )

################################################################################
