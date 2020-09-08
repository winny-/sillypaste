release: python manage.py migrate; yes y | python manage.py populate_languages
web: gunicorn sillypaste.wsgi
