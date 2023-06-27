import streamlit as st

st.sidebar.success("Select a category.")
image_path = "images/mex_map.jpg"

st.write(
    "Mexico (Spanish: México), officially the United Mexican States, is a country in the southern portion of North America. "
    "It is bordered to the north by the United States; to the south and west by the Pacific Ocean; to the southeast by Guatemala"
    ", Belize, and the Caribbean Sea; and to the east by the Gulf of Mexico."
)

st.image(image_path, caption="Map of Mexico", use_column_width=True)
st.write(
    "We will use the API of the National Institute of Statistics and Geography (INEGI) to obtain the information displayed in this page."
)
