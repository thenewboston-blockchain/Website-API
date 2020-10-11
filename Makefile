test:
	docker-compose run app pytest

lint:
	docker-compose run app flake8
