# corona
A simple graph display about the covid-19 spread in Poland.

This app gathers data every 15minutes.

## Used packages
1. Flask
2. Dash
3. Celery
4. Redis [Optional, you can use a different broker]

## installation
add a `.env` file with a following content:

`export BROKER_URL=path_to_broker_url`

## Usage
1. Start your broker for example: `docker start redis`
2. Start a celery worker with celery beat: `celery -A app worker -l info -B`
3. Start the app: `python manage.py` [for production use please checkout passenger_wsgi.py]
