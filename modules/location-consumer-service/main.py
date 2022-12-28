import time
from concurrent import futures
import os
import sys
# Append parent directory to import path
sys.path.append('../../modules')

import grpc
import common.proto.location_pb2 as location_pb2
import common.proto.location_pb2_grpc as location_pb2_grpc
from common.models import Location
import json
from datetime import datetime

from common.config import config_by_name
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from geoalchemy2.functions import ST_AsText, ST_Point
from kafka import KafkaConsumer

# Initialize DB
ENV = os.getenv("ENV", "test")
config = config_by_name[ENV or "test"]
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
db = scoped_session(sessionmaker(bind=engine))

def create_location(message):
    print("Create Location | Start: {0}".message)
    try:
        new_location = Location()
        new_location.person_id = message["person_id"]
        new_location.creation_time = datetime.fromtimestamp(message["creation_time"])
        new_location.coordinate = ST_Point(message["latitude"],message["longitude"])
        db.add(new_location)
        db.commit()
        
        print("Created location {0}".format(new_location.id))
    except Exception as e:
        print(e)
        db.rollback()
        return None

def consume_message():
        consumer = KafkaConsumer(
            bootstrap_servers=[config.KAFKA_SERVER], auto_offset_reset='earliest', api_version=(0, 10, 1)
        )
        consumer.subscribe(config.LOCATION_TOPIC_NAME)
        print("Connected")
        while True:
            try:
                records = consumer.poll(timeout_ms=1000)
    
                for topic_data, consumer_records in records.items():
                    for consumer_record in consumer_records:
                        print("Received message: " + str(consumer_record.value.decode('utf-8')))
                        CreateLocation(json.loads(consumer_record.value.decode('utf-8')))
                continue
            except Exception as e:
                print(e)
                continue

consume_message()