import streamlit as st

st.title("Julian's Weather and Air Quality Application")
st.subheader(
    "Using Streamlit & AirVisual API"
)

option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"))

st.write(option, "chosen." )
