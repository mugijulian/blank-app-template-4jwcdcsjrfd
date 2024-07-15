import streamlit as st
import requests
pip install git+https://github.com/streamlit/streamlit-folium.git



api_key="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"

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")


@st.cache_data
def map_creator(latitude,longitude):
    from streamlit_folium import folium_static
    import folium

    # center on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # add marker for the station
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)

@st.cache_data
def generate_list_of_countries():
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    # st.write(countries_dict)
    return countries_dict

@st.cache_data
def generate_list_of_states(country_selected):
    states_url = f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
    states_dict = requests.get(states_url).json()
    # st.write(states_dict)
    return states_dict

@st.cache_data
def generate_list_of_cities(state_selected,country_selected):
    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
    cities_dict = requests.get(cities_url).json()
    # st.write(cities_dict)
    return cities_dict

#TODO: Include a select box for the options: ["By City, State, and Country","By Nearest City (IP Address)","By Latitude and Longitude"]
# and save its selected option in a variable called category

category = st.selectbox(
    "Select option to get data:",
    ["By City, State, and Country", "By Nearest City (IP Address)", "By Latitude and Longitude"]
)

if category == "By City, State, and Country":
    countries_dict=generate_list_of_countries()
    if countries_dict["status"] == "success":
        countries_list=[]
        for i in countries_dict["data"]:
            countries_list.append(i["country"])
        countries_list.insert(0,"")

        country_selected = st.selectbox("Select a country", options=
                                        countries_list)
        if country_selected:
            # TODO: Generate the list of states, and add a select box for the user to choose the state

            states_dict = generate_list_of_states(country_selected)
            if states_dict["status"] == "success":
                states_list = [i["state"] for i in states_dict["data"]]
                states_list.insert(0, "")
            
                state_selected = st.selectbox("Select a state", options=states_list)
                if state_selected:
                    cities_dict = generate_list_of_cities(state_selected, country_selected)
                    if cities_dict["status"] == "success":
                        cities_list = [i["city"] for i in cities_dict["data"]]
                        cities_list.insert(0, "")

                    # TODO: Generate the list of cities, and add a select box for the user to choose the city
                        city_selected = st.selectbox("Select a city", options=cities_list)
                        if city_selected:
                            aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
                            aqi_data_dict = requests.get(aqi_data_url).json()

                            if aqi_data_dict["status"] == "success":
                                # TODO: Display the weather and air quality data as shown in the video and description of the assignment
                                data = aqi_data_dict["data"]
                                st.subheader(f"Weather and Air Quality for {city_selected}, {state_selected}, {country_selected}")
                                st.write(f"Temperature: {data['current']['weather']['tp']} °C")
                                st.write(f"Humidity: {data['current']['weather']['hu']} %")
                                st.write(f"Wind Speed: {data['current']['weather']['ws']} m/s")
                                st.write(f"Air Quality Index: {data['current']['pollution']['aqius']}")
                                map_creator(data['location']['coordinates'][1], data['location']['coordinates'][0])
                            else:
                                st.warning("No data available for this location.")

                    else:
                        st.warning("No stations available, please select another state.")
            else:
                st.warning("No stations available, please select another country.")
    else:
        st.error("Too many requests. Wait for a few minutes before your next API call.")

elif category == "By Nearest City (IP Address)":
    url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
    aqi_data_dict = requests.get(url).json()

    if aqi_data_dict["status"] == "success":
    # TODO: Display the weather and air quality data as shown in the video and description of the assignment
        data = aqi_data_dict["data"]
        st.subheader("Weather and Air Quality for Your Nearest City")
        st.write(f"City: {data['city']}")
        st.write(f"State: {data['state']}")
        st.write(f"Country: {data['country']}")
        st.write(f"Temperature: {data['current']['weather']['tp']} °C")
        st.write(f"Humidity: {data['current']['weather']['hu']} %")
        st.write(f"Wind Speed: {data['current']['weather']['ws']} m/s")
        st.write(f"Air Quality Index: {data['current']['pollution']['aqius']}")
        map_creator(data['location']['coordinates'][1], data['location']['coordinates'][0])
    else:
        st.warning("No data available for this location.")

elif category == "By Latitude and Longitude":
    # TODO: Add two text input boxes for the user to enter the latitude and longitude information
    latitude = st.text_input("Enter latitude")
    longitude = st.text_input("Enter longitude")
    
    if latitude and longitude:
        url = f"https://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={api_key}"
        aqi_data_dict = requests.get(url).json()

        if aqi_data_dict["status"] == "success":
        # TODO: Display the weather and air quality data as shown in the video and description of the assignment

            data = aqi_data_dict["data"]
            st.subheader("Weather and Air Quality for Provided Coordinates")
            st.write(f"City: {data['city']}")
            st.write(f"State: {data['state']}")
            st.write(f"Country: {data['country']}")
            st.write(f"Temperature: {data['current']['weather']['tp']} °C")
            st.write(f"Humidity: {data['current']['weather']['hu']} %")
            st.write(f"Wind Speed: {data['current']['weather']['ws']} m/s")
            st.write(f"Air Quality Index: {data['current']['pollution']['aqius']}")
            map_creator(data['location']['coordinates'][1], data['location']['coordinates'][0])

        else:
            st.warning("No data available for this location.")
