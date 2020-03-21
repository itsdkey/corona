import csv
from datetime import date

from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError, Timeout


def write_to_csv() -> None:
    """Write data to csv file."""
    past_data = read_from_csv()
    actual_data = get_actual_state()
    gathered_data = {**past_data, **actual_data}
    field_names = ['date', 'cases', 'recovered', 'deaths']
    with open('corona.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for key, value in gathered_data.items():
            writer.writerow({'date': key, **value})


def read_from_csv() -> dict:
    """Read data from a csv file."""
    data = {}
    with open('corona.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = row['date']
            data[date] = {
                'cases': row['cases'],
                'recovered': row['recovered'],
                'deaths': row['deaths'],
            }
    data = unpack_csv_data(data)
    return data


def get_actual_state() -> dict:
    """Get actual data from 'https://www.worldometers.info/coronavirus/country/poland/'."""
    try:
        response = requests.get('https://www.worldometers.info/coronavirus/country/poland/')
    except (ConnectionError, Timeout):
        return {}

    scrapped = {}
    soup = BeautifulSoup(response.content, 'html.parser')
    counters = soup.find_all('div', id='maincounter-wrap')
    for html_element in counters:
        title = html_element.h1.text.lower().strip().replace(':', '')
        value = int(html_element.div.span.text.strip())
        if 'cases' in title:
            scrapped['cases'] = value
        else:
            scrapped[title] = int(value)
    gathered_data = {
        str(date.today()): scrapped,
    }
    return gathered_data


def unpack_csv_data(csv_data: dict) -> dict:
    """Unpack data from a csv to 3 datasets.

    :param csv_data: data from a csv file
    """
    datasets = {
        'cases': {},
        'deaths': {},
        'recovered': {},
    }
    for key, value in csv_data.items():
        datasets['cases'][key] = value['cases']
        datasets['deaths'][key] = value['deaths']
        datasets['recovered'][key] = value['recovered']
    return datasets
