FROM python:3.11-alpine
WORKDIR /app
COPY . .
RUN apk add --no-cache postgresql-libs &&\
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN mv /app/deploy/docker-entrypoint.sh /app &&\
    rm -rf /app/deploy /app/tests
RUN pip install --no-cache-dir --upgrade -r requirements.txt &&\
    pip install --no-cache-dir alembic
ENTRYPOINT ["/app/docker-entrypoint.sh"]

