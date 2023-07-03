import streamlit as st

st.set_page_config(layout="wide")


from utils.urls import urls
from utils.APIClient import APIClient

from utils.data_manipulation import create_salary_df, filter_salary_df, group_salary_df
from utils.data_visulizations import make_salary_distribution_plot
from utils.helpers import get_token

token = get_token("utils/mex_api.txt")
client = APIClient(token, urls)

salary_by_range, salary_dates = client.get_observation(
    "inac/1/2-3/3-5/5+/no/unk/salary_population"
)
salary_df = create_salary_df(salary_by_range, salary_dates)

st.title("Mexico Salary")

st.write(
    "Mexico is considered as the 15th largest economy in the world, while leading exporter in the Latin America."
    "It has a Gross Domestic Product (GDP) of \$1,269 billion, with a nominal GDP of \$9,946. As an emerging global player in the economy,"
    "Mexico has a Foreign Direct Investment of \$29.3 billion placing 19th in the World Export Ranking."
    "Mexico is becoming a fundamentally middle-class country with 50 percent of its population as middle class,"
    "and 30 percent being in the upper class. Ideally, the economy of Mexico will continue to prosper for the following years."
    "The following graph shows the salary distribution in Mexico."
)

col1, col2, col3 = st.columns([1, 1, 1])


with col1:
    filter = st.selectbox("Select a filter", ["None", "Per year"])
    show_full_info = st.checkbox("Show full info", value=False)

if filter == "Per year":
    filtered_salary_df = group_salary_df(salary_df)
else:
    filtered_salary_df = salary_df

with col2:
    start_year_salary_df = st.selectbox(
        "Start date", filtered_salary_df.index.tolist(), index=0
    )
    end_year_salary_df = st.selectbox(
        "End date",
        filtered_salary_df.index.tolist(),
        index=len(filtered_salary_df.index) - 1,
    )

with col3:
    start_range_salary_df = st.selectbox(
        "Start salary", filtered_salary_df.columns.tolist(), index=0
    )
    end_range_salary_df = st.selectbox(
        "End salary",
        filtered_salary_df.columns.tolist(),
        index=len(filtered_salary_df.columns) - 1,
    )

filtered_salary_df = filter_salary_df(
    filtered_salary_df,
    start_year_salary_df,
    end_year_salary_df,
    start_range_salary_df,
    end_range_salary_df,
)

if show_full_info:
    st.write(
        "**The '/no' notation after a year indicates the corresponding quarter for that particular year.**"
    )
    st.dataframe(filtered_salary_df, use_container_width=True)


make_salary_distribution_plot(filtered_salary_df)
