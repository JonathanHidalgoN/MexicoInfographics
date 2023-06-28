import streamlit as st

st.set_page_config(layout="wide")
st.title("Mexico data explorer")

st.sidebar.success("Select a category.")
image_path = "images/mex_map.jpg"

st.write(
    "Mexico (Spanish: México), officially the United Mexican States, is a country in the southern portion of North America. "
    "It is bordered to the north by the United States; to the south and west by the Pacific Ocean; to the southeast by Guatemala"
    ", Belize, and the Caribbean Sea; and to the east by the Gulf of Mexico."
)

try:
    st.image(image_path, caption="Map of Mexico", use_column_width=False)
except:
    st.image(
        st.secrets["map_url"],
        caption="Map of Mexico",
        use_column_width=False,
    )

st.write(
    "Mēxihco is the Nahuatl term for the heartland of the Aztec Empire, namely the Valley of Mexico \
    and surrounding territories, with its people being known as the Mexica.\
    The name came to apply to the territory controlled by the Aztec Empire, which extended from the Atlantic Ocean to the Pacific Ocean, "
    "from central Mexico southwards. "
)


st.write(
    "We will use the API of the National Institute of Statistics and Geography (INEGI) to obtain the information displayed in this page."
)
