if __name__ == "__main__":

    import streamlit as st

    st.set_page_config(layout="wide")
    from pandas import DataFrame
    from asyncio import run as asyncio_run
    from utils.urls import urls, population_dict
    from utils.APIClient import APIClient

    from utils.data_visulizations import (
        plot_cut_age_dataframe,
        make_population_plot,
        population_counter,
        make_population_distribution_plot,
        load_mexico_map,
    )

    from utils.data_manipulation import (
        create_age_data_frame,
        cut_age_dataframe,
    )

    from utils.helpers import (
        get_token,
        create_population_age_labels_sex,
        request_mexico_graph_info,
        extract_state_names,
    )

    ################################################################################
    #                                WEB VARIABLES                                 #
    web_variables = {
        "token": get_token("utils/mex_api.txt"),
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
    age_male_female_dataframe = create_age_data_frame(web_variables, client)
    population_age_labels = (
        web_variables["population_age_labels_1"]
        + web_variables["population_age_labels_2"]
        + web_variables["population_age_labels_3"]
    )
    mexico_info = request_mexico_graph_info()
    state_names = extract_state_names(mexico_info)
    state_df = DataFrame(population_dict.items(), columns=["State", "Population"])
    ################################################################################
    ################################################################################
    #                                WEB STRUCTURE                                 #
    st.title("Mexico population infographic")
    col1, col2 = st.columns(2)

    with col1:
        st.write("## Population")

    st.write(
        "With a population of over 126 million, it is the 10th-most-populous country and has the most Spanish speakers."
        " Mexico is organized as a federal republic comprising 31 states and Mexico City, its capital."
    )

    make_population_plot(client)

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
        age_population_filter = st.selectbox(
            "Population filter", ["None", "Sex"], index=0
        )
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

    st.title("Mexico population distribution")

    st.write(
        "Mexico has a dynamic population that is undergoing a gradual transition from a youthful demographic to an aging one. "
        "As of 2020, approximately 24.95 percent of Mexico's population fell within the age group of 0 to 14 years, reflecting a significant "
        "proportion of young individuals. The majority, accounting for around 66.91 percent, belonged to the working-age group of 15 to 64 years, "
        "indicating a productive segment of the population. Additionally, about 8.13 percent of Mexico's population were 65 years or older, "
        "signifying the presence of an elderly population."
    )

    col7, col8 = st.columns(2)

    with col7:
        distribution_year = st.selectbox(
            "Year", web_variables["population_age_years"], index=0
        )
    with col8:
        age_distribution_filter = st.selectbox(
            "Distribution filter", ["None", "Sex"], index=0
        )

    if age_distribution_filter == "Sex":
        make_population_distribution_plot(age_male_female_dataframe, distribution_year)
    else:
        make_population_distribution_plot(
            cut_age_dataframe(
                distribution_year,
                distribution_year,
                web_variables["population_age_range"][0],
                web_variables["population_age_range"][-1],
                age_male_female_dataframe,
                filter=age_distribution_filter,
            ),
            distribution_year,
        )

    col9, col10 = st.columns([1, 2])
    with col9:
        st.dataframe(
            state_df.sort_values(by=["Population"], ascending=False).reset_index(
                drop=True
            )
        )
    with col10:
        load_mexico_map(mexico_info, state_df, "Population")

    with col2:
        # Async do not work with streamlit, put this in the end of the script,
        # the col will keep in the same place
        t = st.empty()
        asyncio_run(
            population_counter(t=t, children_per_second=21, population=population)
        )

################################################################################
