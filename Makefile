.PHONY: startdb stopdb dblogs migrate run

run:
	uvicorn main:app --reload

migrate:
# Create your migration with "alembic revision --autogenerate -m 'Migration name'"
	alembic upgrade head

startdb:
	docker compose -f docker-compose-dev.yml up -d
	@echo "PgAdmin may take a while, but will be accessible in port 5433."
	@echo "Don't forget to create a database called 'teste-workalove'!"

stopdb:
	docker compose -f docker-compose-dev.yml down
	docker compose -f docker-compose-dev.yml rm -fsv

dblogs:
	docker compose -f docker-compose-dev.yml logs

