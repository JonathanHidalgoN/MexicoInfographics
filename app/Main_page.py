import streamlit as st

st.set_page_config(layout="wide")


from utils.helpers import request_mexico_graph_info, extract_state_names
from utils.data_manipulation import create_state_df
from utils.data_visulizations import load_mexico_map

mexico_info = request_mexico_graph_info()
state_names = extract_state_names(mexico_info)
df = create_state_df(state_names)

st.sidebar.success("Select a category.")
st.title("Mexico Infographic")

st.write(
    "Welcome to the Mexico Exploration Page! Here, you can embark on an interactive journey to discover and learn about Mexico through engaging \
    visualizations and graphs. The information presented on this page is sourced from the INEGI (National Institute of Statistics and Geography) \
    API, ensuring accurate and reliable data. Immerse \
    yourself in the rich cultural, geographical, and demographic aspects of Mexico with our interactive tools and explore the \
    fascinating diversity of this vibrant country."
)

load_mexico_map(mexico_info, df)

st.write(
    "Mexico (Spanish: México), officially the United Mexican States, is a country in the southern portion of North America. "
    "It is bordered to the north by the United States; to the south and west by the Pacific Ocean; to the southeast by Guatemala"
    ", Belize, and the Caribbean Sea; and to the east by the Gulf of Mexico."
)

st.write(
    "Mēxihco is the Nahuatl term for the heartland of the Aztec Empire, namely the Valley of Mexico \
    and surrounding territories, with its people being known as the Mexica.\
    The name came to apply to the territory controlled by the Aztec Empire, which extended from the Atlantic Ocean to the Pacific Ocean, "
    "from central Mexico southwards. "
)
