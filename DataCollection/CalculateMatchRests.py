import pandas as pd
from datetime import datetime, timedelta


def preprocess_fixtures(fixtures):
    """Preprocess the fixtures data."""
    fixtures.rename(columns={'Distance': 'Away_Distance'}, inplace=True)
    fixtures.drop(['Wk'], axis=1, inplace=True)
    fixtures['Home_Rest'] = 0
    fixtures['Away_Rest'] = 0

    for i in range(len(fixtures)):
        date = fixtures['Date'][i]
        time = fixtures['Time'][i]  
        datetime_str = date + ' ' + time
        fixtures.at[i, 'Date'] = datetime.strptime(datetime_str, '%d-%m-%Y %H:%M')
    return fixtures

def calculate_rest_days(fixtures, target_column):
    """Calculate rest days for teams."""
    for index, row in fixtures.iloc[20:].iterrows():
        current_value = row[target_column]
        previous_home_index = fixtures.loc[:index - 1, 'Home'][fixtures['Home'] == current_value].last_valid_index()
        previous_away_index = fixtures.loc[:index - 1, 'Away'][fixtures['Away'] == current_value].last_valid_index()

        if pd.isna(previous_home_index) or pd.isna(previous_away_index):
            fixtures.at[index, f'{target_column}_Rest'] = 7
        else:
            if (previous_home_index > previous_away_index):
                previous_date = fixtures.loc[previous_home_index, 'Date']
            else:
                previous_date = fixtures.loc[previous_away_index, 'Date']
            
            current_date = fixtures.loc[index, 'Date']
            delta = (current_date - previous_date).days
            fixtures.at[index, f'{target_column}_Rest'] = delta

    fixtures.loc[:20, f'{target_column}_Rest'] = 7  # Ensure the first 20 rows have a rest value of 7
    return fixtures


def main():
    fixtures_file_path = '/Users/footballdata_distance.csv'
    fixtures = pd.read_csv(fixtures_file_path)
    
    if fixtures.empty:
        print("No data loaded.")
        return

    fixtures = preprocess_fixtures(fixtures)
    fixtures = calculate_rest_days(fixtures, 'Home')
    fixtures = calculate_rest_days(fixtures, 'Away')

    fixtures.to_csv('/Users/footballdata_rest.csv', index=False)

if __name__ == "__main__":
    main()
