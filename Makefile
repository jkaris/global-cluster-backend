migrate:
	python manage.py migrate --noinput

makemigrations: makemigrations
	python manage.py loaddata sample_admin

createsuperuser:
	python manage.py createsuperuser

runserver:
	python manage.py runserver
