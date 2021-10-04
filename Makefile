lint:
	flake8 .

migrations:
	python manage.py makemigrations
	python manage.py migrate

shell:
	python manage.py shell_plus

tests:
	python manage.py test -v 2 --keepdb

tests-coverage:
	coverage run manage.py test -v 2 --keepdb
	coverage report -m
	coverage html

dispatch:
	@python ./scripts/dispatcher.py -e ${EVENTS}
