.PHONY: migrations
migrations:
	docker-compose exec server python manage.py makemigrations

.PHONY: migrate
migrate:
	docker-compose exec server python manage.py migrate

.PHONY: test
test:
	docker-compose run server pytest --ds core.settings.test -s

.PHONY: shell
shell:
	docker-compose exec server python manage.py shell
