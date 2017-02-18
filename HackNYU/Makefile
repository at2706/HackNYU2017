build:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver
run:
	python manage.py runserver

reset:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

clean:
	find -type f -name "*.pyc" -delete
	find -type f -name "*.DS_Store" -delete