FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY ./location/requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

#ENV PYTHONUNBUFFERED=1

COPY ./common ./common
COPY . .
CMD ["python", "location/main.py"]