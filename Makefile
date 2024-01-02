.PHONY: startdb stopdb dblogs migrate run

################################################################################
#                              I M P O R T A N T                               #
#                                                                              #
# Make sure you create a Python virtual environment and install the project    #
# dependencies before running any target, or some tools may not work properly. #
#                                                                              #
#  $ python3 -m venv env                                                       #
#  $ source env/bin/activate                                                   #
#  $ pip install -r requirements.txt                                           #
#                                                                              #
################################################################################

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

dbps:
	docker compose -f docker-compose-dev.yml ps

