import csv
from datetime import date
import json

from bs4 import BeautifulSoup
from redis import Redis
import requests
from requests.exceptions import ConnectionError, Timeout

from .settings import REDIS_DATABASE, REDIS_PASSWORD, REDIS_SOCKET_PATH


def write_to_csv(gathered_data: dict) -> None:
    """Write data to csv file.

    :param gathered_data: data gathered during the day in Redis.
    """
    field_names = ['date', 'cases', 'recovered', 'deaths', 'daily_cases']
    cases_overall = 0
    with open('corona.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for key, value in gathered_data.items():
            daily_cases = value['cases'] - cases_overall
            cases_overall = value['cases']
            writer.writerow({'date': key, 'daily_cases': daily_cases, **value})


def read_from_csv() -> dict:
    """Read data from a csv file."""
    data = {}
    with open('corona.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = row['date']
            data[date] = {
                'cases': int(row['cases']),
                'recovered': int(row['recovered']),
                'deaths': int(row['deaths']),
                'daily_cases': int(row['daily_cases']),
            }
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
        value = int(html_element.div.span.text.strip().replace(',', ''))
        if 'cases' in title:
            scrapped['cases'] = value
        else:
            scrapped[title] = int(value)
    gathered_data = {
        str(date.today()): scrapped,
    }
    return gathered_data


def unpack_csv_data(csv_data: dict) -> dict:
    """Unpack data from a csv to 3 data sets.

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


def read_collected_data() -> dict:
    """Read collected data from Redis or the CSV database."""
    with get_redis_instance() as redis:
        if redis.exists('corona-database'):
            collected = json.loads(redis.get('corona-database').decode())
        else:
            collected = read_from_csv()
    return collected


def get_redis_instance() -> Redis:
    """Return a Redis instance with the proper configuration."""
    return Redis(db=REDIS_DATABASE, unix_socket_path=REDIS_SOCKET_PATH, password=REDIS_PASSWORD)
