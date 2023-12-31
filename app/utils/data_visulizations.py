import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


from asyncio import sleep
from pandas import DataFrame


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
        r = await sleep(children_per_second)


def make_population_plot(c_APIclient) -> None:
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

    population_df = DataFrame(
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

    st.plotly_chart(fig, use_container_width=True)


def plot_cut_age_dataframe(cut_dataframe: DataFrame) -> None:
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
    st.plotly_chart(fig, use_container_width=True)


def make_population_distribution_plot(data_frame: DataFrame, year: str) -> None:
    """
    This function plots the population distribution.
    Parameters:
        data_frame (dataframe): The dataframe.
    Returns:
        None
    """
    data = data_frame.loc[str(year)]
    fig = go.Figure(data=[go.Bar(x=data.index, y=data.values)])

    fig.update_layout(
        title=f"Population Distribution - {year}",
        xaxis_title="Age Group",
        yaxis_title="Population",
    )

    st.plotly_chart(fig, use_container_width=True)


def load_mexico_map(
    mexico_regions: dict,
    state_df: DataFrame,
    target_name: str = "Value",
    show_values: bool = True,
):
    """
    This function loads the map of Mexico.
    A dataframe is used to color the map, color is based on the value column.
    Parameters:
        mexico_regions (dict): The dictionary of Mexico regions.
        state_df (dataframe): The dataframe of the states.
        target_name (str): The name of the target column.
        show_values (bool): Whether to show the values column on the map. Default is True.
    Returns:
        None
    """
    fig = px.choropleth(
        geojson=mexico_regions,
        locations=state_df["State"],
        data_frame=state_df,
        color=target_name,
        color_continuous_scale="Oryel",
        featureidkey="properties.name",
    )
    fig.update_geos(
        showcountries=False, showcoastlines=False, showland=True, fitbounds="locations"
    )

    if show_values:
        fig.update_layout(
            coloraxis_showscale=True,
        )
    st.plotly_chart(fig, use_container_width=True)


def make_salary_distribution_plot(salary_df: DataFrame) -> None:
    """
    This function plots the salary distribution.
    Parameters:
        salary_df (dataframe): The dataframe.
    Returns:
        None
    """
    fig = px.bar(salary_df, x=salary_df.index, y=salary_df.columns, barmode="group")
    fig.update_layout(
        title="Salary Distribution in Mexico",
        xaxis_title="Date",
        yaxis_title="Number of People",
        legend_title="Salary Range",
    )
    st.plotly_chart(fig, use_container_width=True)
