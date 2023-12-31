from pandas import DataFrame


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


def create_age_data_frame(web_variables: dict, client: any) -> DataFrame:
    """
    This function creates a dataframe with the population per age.
    Parameters:
        web_variables (dict): The web variables.
        client (any): The APIClient object.
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
    dataframe = DataFrame(population_age, index=date)
    return dataframe


def add_age_data_frame(dataframe: DataFrame) -> DataFrame:
    """
    This funcition merge age columns in the dataframe.
    Parameters:
        dataframe (dataframe): The dataframe to merge.
    Returns:
        dataframe: The dataframe with the merged columns.
    """
    age_dataframe = dataframe.copy()
    col_names = age_dataframe.columns
    new_col_names = []

    for idx, col_name in enumerate(col_names):
        if idx % 2 == 0:
            tmp = col_name.split(" ")
            new_col_names.append(tmp[0] + " years")

    for idx, col_name in enumerate(col_names):
        if idx % 2 != 0:
            age_dataframe[new_col_names[idx // 2]] = (
                age_dataframe[col_name] + age_dataframe[col_names[idx - 1]]
            )

    for col_name in col_names:
        age_dataframe.drop(col_name, axis=1, inplace=True)

    return age_dataframe


def cut_age_dataframe(
    start_year: int,
    end_year: int,
    start_age: str,
    end_age: str,
    original_df: DataFrame,
    filter: str,
) -> DataFrame:
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
        # Working on summing the columns
        return add_age_data_frame(selected_data_frame)


def create_salary_df(salary_by_range: dict, dates: dict) -> DataFrame:
    """
    This function creates a dataframe with the salary by range.
    Parameters:
        salary_by_range (dict): The salary by range.
        dates (dict): The dates.
    Returns:
        dataframe: The dataframe with the salary by range.
    """
    assert len(salary_by_range) == len(
        dates
    ), "The length of the salary by range and dates are not the same"
    col_names = dates["0"]
    index_names = [
        "Not working",
        "Less or 1 MW",
        "1 to 2 MW",
        "2 to 3 MW",
        "3 to 5 MW",
        "More than 5 MW",
        "No income",
        "No answer" "",
    ]
    salary_df = DataFrame(salary_by_range, index=col_names)
    salary_df.index.name = "Date"
    salary_df.columns = index_names
    return salary_df


def create_state_df(states: list[str], values: list = None) -> DataFrame:
    """
    This function creates a dataframe with dummy values for each state.
    Parameters:
        states (list[str]): The list of states.
        values (list): The list of values.
    Returns:
        state_df (dataframe): The dataframe.
    """
    if values is None:
        MEX_NUM_STATES = 32
        values = [i for i in range(MEX_NUM_STATES)]
    state_df = DataFrame({"State": states, "Value": values})
    return state_df


def group_salary_df(salary_df: DataFrame) -> DataFrame:
    """
    This function groups the salary dataframe by year.
    Parameters:
        salary_df (dataframe): The salary dataframe.
    Returns:
        dataframe: The grouped salary dataframe.
    """
    copy_df = salary_df.copy()
    years = [str(year).split("/")[0] for year in salary_df.index.tolist()]
    years = list(dict.fromkeys(years))
    for year in years:
        match = [
            str(df_year)
            for df_year in salary_df.index.tolist()
            if year == df_year.split("/")[0]
        ]
        row_values = copy_df.loc[match].sum(axis=0) / len(match)
        copy_df.loc[year] = row_values
    return copy_df.loc[years]


def filter_salary_df(
    salary_df: DataFrame,
    start_year: int,
    end_year: int,
    start_salary: str,
    end_salary: str,
) -> DataFrame:
    """
    This function filters the salary dataframe by the specified years.
    Parameters:
        salary_df (dataframe): The salary dataframe.
        start_year (int): The start year.
        end_year (int): The end year.
        filter (str): The filter to apply to the dataframe.
        start_salary (str): The start salary.
        end_salary (str): The end salary.
    Returns:
        dataframe: The filtered dataframe.
    """
    copy_df = salary_df.copy()
    return copy_df.loc[str(start_year) : str(end_year), start_salary:end_salary]
