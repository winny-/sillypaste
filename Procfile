release: python manage.py migrate; python manage.py populate_languages --remove-unknown; python manage.py expire
web: gunicorn sillypaste.wsgi
