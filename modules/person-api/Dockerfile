FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY ./person-api/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY ./common ./common
COPY ./person-api ./person-api

WORKDIR ./person-api
CMD ["flask", "run", "--host", "0.0.0.0"]