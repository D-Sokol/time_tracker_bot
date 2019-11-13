web: gunicorn --bind 0.0.0.0:$PORT time_tracker:server
release: ./test.py && flask db upgrade
