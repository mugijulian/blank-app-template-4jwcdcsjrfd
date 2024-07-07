import requests
import streamlit as st

def fetch_countries():
    url = "https://api.airvisual.com/v2/countries?key=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"
    response = requests.get(url)
    data = response.json()
    countries = [country['country'] for country in data['data']]
    return countries

def main():

st.title("Julian's Weather and Air Quality Application")
st.subheader(
    "Using Streamlit & AirVisual API"
)

countries = fetch_countries()

option = st.selectbox(
    "Choose a country: ",
    countries;
    index = None,
    placeholder = "Select country..",
)
    
    

st.write(option, "chosen." )
