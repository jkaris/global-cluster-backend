migrate:
	DJANGO_SETTINGS_MODULE=global_cluster_backend.settings.base python manage.py migrate --noinput

makemigrations: makemigrations
	DJANGO_SETTINGS_MODULE=global_cluster_backend.settings.base python manage.py makemigrations

createsuperuser:
	DJANGO_SETTINGS_MODULE=global_cluster_backend.settings.base python manage.py createsuperuser

runserver:
	DJANGO_SETTINGS_MODULE=global_cluster_backend.settings.base python manage.py runserver
