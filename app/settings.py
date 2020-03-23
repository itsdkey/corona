import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

UPDATE_INTERVAL = 1000 * 60 * 15

COLUMN_TRANSLATION = [
    ('date', 'data'),
    ('cases', 'łączna liczba przypadków'),
    ('growth_factor', 'współczynnik wzrostu'),
    ('recovered', 'łączna liczba wyzdrowiało'),
    ('deaths', 'łączna liczba zgonów'),
]
