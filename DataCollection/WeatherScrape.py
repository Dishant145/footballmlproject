import pandas as pd
import requests
import os

def reformat_date(date_str):
    """Reformat the date string to the required format."""
    date_part, time_part = date_str.split('T')
    day, month, year = date_part.split('-')[::-1]
    return f"{day}-{month}-{year}T{time_part}:00"

def update_dates(data):
    """Update the date format for the DataFrame."""
    data['Date'] = data['Date'].apply(reformat_date)
    return data

def fetch_weather_data(api_key, date, lat, lon):
    """Fetch weather data from the API for a given date and location."""
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/{date}?key={api_key}&include=current&contentType=csv"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        print(f"Error fetching weather data for {lat}, {lon} on {date}: {e}")
        return None

def main():
    input_file = '/Users/Disha/final_fixture2.csv'
    api_key = 'CXMP47QL58CJ8PZ8FVTLCWGRX'

    data = pd.read_csv(input_file)
    data = update_dates(data)

    all_weather_data = []

    for i, row in data.iterrows():
        date = row['Date']
        lat = row['lat']
        lon = row['lon']
        csv_content = fetch_weather_data(api_key, date, lat, lon)
        if csv_content:
            # Read CSV content into DataFrame
            weather_data = pd.read_csv(pd.compat.StringIO(csv_content))
            # Add an index column to identify the original row
            weather_data['Index'] = i
            all_weather_data.append(weather_data)

    if all_weather_data:
        # Concatenate all weather data into a single DataFrame
        consolidated_weather_data = pd.concat(all_weather_data, ignore_index=True)
        # Select relevant columns
        weather_columns = ['temp', 'humidity', 'windspeed', 'sealevelpressure', 'conditions']
        consolidated_weather_data = consolidated_weather_data[['Index'] + weather_columns]

        # Update the main data with weather information
        for col in weather_columns:
            data[col] = 0  # Initialize columns in main data

        for i, row in consolidated_weather_data.iterrows():
            index = int(row['Index'])
            for col in weather_columns:
                data.at[index, col] = row[col]

    data.to_csv(input_file, index=False)
    print(f"Updated data saved to {input_file}")

if __name__ == "__main__":
    main()
