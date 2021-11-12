prepare:
	python manage.py collectstatic
	python manage.py migrate
	python manage.py populate_languages --remove-unknown
	python manage.py expire

host:
	gunicorn sillypaste.wsgi

dev: prepare
	python manage.py runserver

.PHONY: prepare host dev
