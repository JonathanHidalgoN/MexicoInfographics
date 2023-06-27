if __name__ == "__main__":

    import streamlit as st

    from asyncio import run as asyncio_run
    from urls import urls
    from APIClient import APIClient

    from utils.Visualizations import (
        plot_cut_age_dataframe,
        make_population_distribution_plot,
        population_counter,
    )

    from utils.DataManipulation import (
        get_token,
        create_age_data_frame,
        cut_age_dataframe,
        create_population_age_labels_sex,
        create_salary_df
    )

    ################################################################################
    #                                WEB VARIABLES                                 #
    web_variables = {
        "map_image_path": "images/mex_map.jpg",
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
    age_male_female_dataframe = create_age_data_frame(web_variables, client)
    population_age_labels = (
        web_variables["population_age_labels_1"]
        + web_variables["population_age_labels_2"]
        + web_variables["population_age_labels_3"]
    )
    salary_by_range, salary_dates = client.get_observation("inac/1/2-3/3-5/5+/no/unk/salary_population")
    salary_df = create_salary_df(salary_by_range, salary_dates)
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

    st.dataframe(salary_df)

    with col2:
        # Async do not work with streamlit, put this in the end of the script,
        # the col will keep in the same place
        t = st.empty()
        asyncio_run(
            population_counter(t=t, children_per_second=21, population=population)
        )

################################################################################
