import streamlit as st

st.title("Julian's Weather and Air Quality Application")
st.subheader(
    "Using Streamlit & AirVisual API"
)

option = st.selectbox(
    "Select a country please: ",
    (http://api.airvisual.com/v2/countries?key={{YOUR_API_KEY}}))
