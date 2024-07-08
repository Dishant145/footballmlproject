import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

def get_page_content(url):
    """Fetching page content from URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_table(content):
    """Parsing the main table from the content."""
    soup = BeautifulSoup(content, "lxml")
    table = soup.find("table", {"id": "seasons"})
    return table

def get_season_links(table):
    """Extracting season URLs from the table."""
    data = []
    for row in table.find_all("tr")[2:7]:  
        cells = row.find_all("td")
        data.append([cell.find("a")["href"] if cell.find("a") else "" for cell in cells])

    seasons = []
    for row in data:
        row[0] = row[0].replace('-Stats', '-Scores-and-Fixtures')
        url = "https://fbref.com" + row[0][:22] + "schedule/" + row[0][22:]
        seasons.append(url)
        
    return seasons

def scrape(url):
    """Function to scrape season links from a URL."""
    content = get_page_content(url)
    if content:
        table = parse_table(content)
        if table:
            return get_season_links(table)
    return []

def get_match_report_links(url):
    """Extracting match report links from a season URL."""
    content = get_page_content(url)
    if content:
        soup = BeautifulSoup(content, "lxml")
        table = soup.find("table")

        data = []
        for row in table.find_all("tr"):
            for col in table.find_all("th")[12:13]: 
                cells = row.find_all("td")
                data.append([cell.find("a")["href"] if cell.find("a") else "" for cell in cells])

        report = []
        for row in data[1:]:
            if row[-2] != "":
                url = "https://fbref.com" + row[-2]
                report.append(url)
        return report
    return []
    
def get_expected_assisted__goals(url, index):
    """Extracting Expected Assisted Goals from a match report URL."""
    stats = pd.read_html(url)
    stats_table = stats[index].droplevel(level=0, axis=1)
    return stats_table["xAG"].iloc[-1]

def scrape_fixture_data(urls):
    """Scraping fixture data from the list of season URLs."""
    combined_fixture = pd.DataFrame()
    for url in reversed(urls):
        fixture = pd.read_html(url)[0]
        combined_fixture = pd.concat([combined_fixture, fixture])
    combined_fixture = combined_fixture.reset_index(drop=True)
    combined_fixture = combined_fixture.drop(['Attendance', 'Notes', 'Match Report'], axis=1)
    combined_fixture = combined_fixture.dropna()
    return combined_fixture

def scrape_match_reports(englandfixture):
    """Scraping numeric data for each fixture."""
    homeag = []
    awayag = []
    for i in englandfixture:
        urls = get_match_report_links(i)
        time.sleep(2)
        for url in urls:
            homeag.append(get_expected_assisted__goals(url, 4))
            awayag.append(get_expected_assisted__goals(url, 11))
            time.sleep(2)
    return pd.DataFrame(homeag), pd.DataFrame(awayag)

def main():
    # URLs to scrape
    url_england = "https://fbref.com/en/comps/9/history/Premier-League-Seasons"
    # url_spain = "https://fbref.com/en/comps/12/history/La-Liga-Seasons"
    # url_france = "https://fbref.com/en/comps/13/history/Ligue-1-Seasons"
    # url_germany = "https://fbref.com/en/comps/20/history/Bundesliga-Seasons"
    # url_italy  = "https://fbref.com/en/comps/11/history/Serie-A-Seasons"

    # Scraping season links
    england = scrape(url_england)

    # Scraping fixtures data
    combined_fixture = scrape_fixture_data(england)

    # Scraping match reports
    homeag, awayag = scrape_match_reports(england)

    # Combining data and saving to CSV
    combined_fixture = pd.concat([combined_fixture, homeag, awayag], axis=1)
    combined_fixture.columns = list(combined_fixture.columns[:-2]) + ['HomeAG', 'AwayAG']
    combined_fixture.to_csv('/Users/footballdata.csv', index=False)
    logging.info("Scrapping Football Teams")

if __name__ == "__main__":
    main()
