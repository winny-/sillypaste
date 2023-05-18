host:
	gunicorn sillypaste.wsgi

dev: prepare
	python manage.py runserver

.PHONY: prepare host dev
