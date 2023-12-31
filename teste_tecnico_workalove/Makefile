.PHONY: startdb stopdb dblogs migrate

startdb:
	docker compose -f docker-compose-dev.yml up -d
	@echo "PgAdmin may take a while, but will be accessible in port 5433."
	@echo "Don't forget to create a database called 'teste-workalove'!"

stopdb:
	docker compose -f docker-compose-dev.yml down

dblogs:
	docker compose -f docker-compose-dev.yml logs

migrate:
	python manage.py migrate

