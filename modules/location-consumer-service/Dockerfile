FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY ./persist-location-job/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

ENV PYTHONUNBUFFERED=1

COPY ./common ./common
COPY ./persist-location-job ./persist-location-job
CMD ["python", "persist-location-job/main.py"]