import pandas as pd
import numpy as np

def load_data(file_path):
    """Load the data from a CSV file."""
    return pd.read_csv(file_path)

def categorize_fatigue(data):
    """Categorize the fatigue levels for home and away teams."""
    data['Home_Fatigue'] = np.where(data['Home_Rest'] < 3, 'High', 
                                    np.where(data['Home_Rest'] < 7, 'Moderate', 'Low'))
    
    conditions = [
        (data['Away_Rest'] < 7) & (data['Away_Distance'] >= 250),
        ((data['Away_Rest'] < 7) & (data['Away_Distance'] < 250)) | 
        ((data['Away_Rest'] >= 7) & (data['Away_Distance'] >= 250)),
        (data['Away_Rest'] >= 7) & (data['Away_Distance'] < 250)
    ]
    choices = ['High', 'Moderate', 'Low']
    data['Away_Fatigue'] = np.select(conditions, choices, default='Low')
    
def categorize_weather(data):
    """Categorize humidity and wind speed."""
    data['Humidity'] = pd.qcut(data['humiidity'], q=[0, 0.25, 0.5, 0.75, 1], labels=['Low', 'Moderate', 'High'])
    data['Wind'] = pd.qcut(data['windspeed'], q=[0, 0.25, 0.5, 0.75, 1], labels=['Low', 'Moderate', 'High'])

def clean_data(data):
    """Drop unnecessary columns."""
    columns_to_drop = ['Away_Distance', 'Home_Rest', 'Away_Rest', 'temp', 'humidity', 'windspeed', 'Day', 'Time']
    data.drop(columns=columns_to_drop, inplace=True, errors='ignore')

def save_data(data, file_path):
    """Save the cleaned data to a CSV file."""
    data.to_csv(file_path, index=False)

def main():
    input_file_path = '/Users/Disha/final_data_complete_new.csv'
    output_file_path = '/Users/Disha/final_data_new.csv'

    # Load data
    data = load_data(input_file_path)
    
    # Process data
    categorize_fatigue(data)
    categorize_weather(data)
    clean_data(data)
    
    # Save data
    save_data(data, output_file_path)
    print(f"Processed data saved to {output_file_path}")

if __name__ == "__main__":
    main()
