import pandas as pd
from geopy.geocoders import Nominatim

def format_date_time(date_time_str):
    """Formatting date and time string."""
    date, time = date_time_str.split(' ')
    formatted_date_time = date + 'T' + time
    return formatted_date_time

def add_weather_dates(weather_data, fixture_data):
    """Adding formatted date-time from fixture data to weather data."""
    weather_data['Date'] = fixture_data['Date'].apply(format_date_time)
    return weather_data

def get_coordinates(data):
    """Getting latitude and longitude coordinates for venue locations."""
    geolocator = Nominatim(user_agent="MyApp")
    for i, venue in enumerate(data['Home_Venue']):
        location = geolocator.geocode(venue)
        if location:
            data.at[i, 'lat'] = location.latitude
            data.at[i, 'lon'] = location.longitude
        else:
            print(f"Coordinates not found for {venue}")
    return data

def main():
    # Read fixture and weather data
    fixture_file = '/Users/Disha/final_fixture2.csv'
    weather_file = '/Users/Disha/final_weathers2.csv'
    data = pd.read_csv(fixture_file)
    weather_data = pd.read_csv(weather_file)

    # Updating weather data with formatted dates from fixture data
    weather_data = add_weather_dates(weather_data, data)
    
    # Getting coordinates for venues and update data
    data = get_coordinates(data)

    # Save updated weather data
    weather_data.to_csv(weather_file, index=False)
    
    # Save updated fixture data with coordinates
    data.to_csv(fixture_file, index=False)

if __name__ == "__main__":
    main()
