import pandas as pd
import scipy.stats as stats

def load_data(file_path):
    """Load data from a CSV file."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()

def calculate_zscores(data):
    """Calculate z-scores for specified columns."""
    zscores = {
        'CardsPG': stats.zscore(data['CardsPG']),
        'HomeWin': stats.zscore(data['HomeWin']),
        'AwayWin': stats.zscore(data['AwayWin']),
        'Draw': stats.zscore(data['Draw'])
    }
    return zscores

def calculate_referee_score(zscores):
    """Calculate the Referee Score based on z-scores."""
    Referee_Score = (2 * zscores['CardsPG']) + (1 * (zscores['HomeWin'] - zscores['AwayWin'])) + (0.5 * zscores['Draw'])
    return Referee_Score

def assign_referee_bias(data, Referee_Score):
    """Assign Referee Bias based on Referee Score."""
    data['Referee_Bias'] = ""
    for i in range(len(Referee_Score)):
        if Referee_Score[i] < 0:
            data.at[i, 'Referee_Bias'] = "Away"
        elif Referee_Score[i] > 0:
            data.at[i, 'Referee_Bias'] = "Home"
        else:
            data.at[i, 'Referee_Bias'] = "Neutral"
    return data

def clean_data(data):
    """Clean up the data by dropping unnecessary columns."""
    data.drop(['CardsPG', 'HomeWin', 'AwayWin', 'Draw'], axis=1, inplace=True)
    return data

def save_data(data, file_path):
    """Save the processed data to a CSV file."""
    data.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def main():
    file_path = '/Users/Disha/final_data.csv'
    data = load_data(file_path)
    
    if data.empty:
        print("No data loaded.")
        return

    zscores = calculate_zscores(data)
    Referee_Score = calculate_referee_score(zscores)
    data = assign_referee_bias(data, Referee_Score)
    data = clean_data(data)
    
    save_data(data, '/Users/Disha/final_data_complete.csv')

if __name__ == "__main__":
    main()
