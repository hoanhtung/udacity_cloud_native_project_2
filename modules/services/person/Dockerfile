FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY ./location-service/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

ENV PYTHONUNBUFFERED=1

COPY ./common ./common
COPY ./location-service ./location-service
CMD ["python", "location-service/main.py"]