import pandas as pd
import haversine as hs
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")


def geocode_location(venue):
    """Geocode a location to get its latitude and longitude."""
    try:
        location = geolocator.geocode(venue)
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Geocoding failed for: {venue}")
            return None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error for {venue}: {e}")
        return None

def add_away_venue(fixture, unique_rows):
    """Adding unique away venue to fixture data based on home teams."""
    fixture['Away_Venue'] = fixture['Away'].map(unique_rows.set_index('Home')['Home_Venue']).fillna(0)
    return fixture

def calculate_distance(df, col1, col2):
    """Calculating distance between Home and Away venues using Haversine formula."""
    distances = []
    for i in range(len(df)):
        loc1 = geocode_location(df[col1].iloc[i])
        loc2 = geocode_location(df[col2].iloc[i])
        if loc1 and loc2:
            distance = round(hs.haversine(loc1, loc2), 0)
            distances.append(distance)
        else:
            distances.append(None)
    df['Distance'] = distances
    return df

def main():
    file_path = '/Users/footballdata.csv'
    fixture = pd.read_csv(file_path)
    
    if fixture.empty:
        print("No data loaded.")
        return

    fixture = fixture.rename(columns={'Venue': 'Home_Venue'})
    unique_rows = fixture[['Home', 'Home_Venue']].drop_duplicates(subset=['Home', 'Home_Venue']).reset_index(drop=True)
    fixture = add_away_venue(fixture, unique_rows)
    fixture = calculate_distance(fixture, 'Home_Venue', 'Away_Venue')
    
    # Save the updated fixture data
    fixture.to_csv('/Users/footballdata_distance.csv', index=False)
    logging.info("Fixture data with distances saved successfully.")

if __name__ == "__main__":
    main()
