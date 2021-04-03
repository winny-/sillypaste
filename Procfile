release: python manage.py migrate; python manage.py populate_languages --remove-unknown
web: gunicorn sillypaste.wsgi
