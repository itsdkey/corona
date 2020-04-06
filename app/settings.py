import os

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

UPDATE_INTERVAL = 1000 * 60 * 15

COLUMN_TRANSLATION = [
    ('date', 'data'),
    ('cases', 'łączna liczba przypadków'),
    ('growth_factor', 'współczynnik wzrostu'),
    ('recovered', 'łączna liczba wyzdrowiałych'),
    ('deaths', 'łączna liczba zgonów'),
]

REDIS_SOCKET_PATH = os.environ.get('REDIS_SOCKET_PATH', '')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
REDIS_DATABASE = os.environ.get('REDIS_DATABASE', '')
