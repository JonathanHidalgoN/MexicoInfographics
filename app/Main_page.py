import streamlit as st

st.set_page_config(layout="wide")

from information import introduction, info_1, info_2, state_descriptions
from utils.helpers import request_mexico_graph_info, extract_state_names
from utils.data_manipulation import create_state_df
from utils.data_visulizations import load_mexico_map

mexico_info = request_mexico_graph_info()
state_names = extract_state_names(mexico_info)
df = create_state_df(state_names, state_descriptions)

st.sidebar.success("Select a category.")
st.title("Mexico Infographic")

st.write(introduction)

load_mexico_map(mexico_info, df, show_values=False)

st.write(info_1)

st.write(info_2)
