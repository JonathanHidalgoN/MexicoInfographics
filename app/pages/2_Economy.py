import streamlit as st
from utils.urls import urls
from utils.APIClient import APIClient

from utils.DataManipulation import get_token, create_salary_df

token = get_token("utils/mex_api.txt")
client = APIClient(token, urls)

salary_by_range, salary_dates = client.get_observation(
    "inac/1/2-3/3-5/5+/no/unk/salary_population"
)
salary_df = create_salary_df(salary_by_range, salary_dates)

st.dataframe(salary_df)
