import time
from concurrent import futures
import os
import sys
sys.path.append(os.path.abspath('../'))

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
from kafka import KafkaProducer
import logging

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
class LocationService(location_pb2_grpc.LocationServiceServicer):
    def Retrieve(self, request, context):
        logging.info("Retrieve location start")
        try:
            location, coord_text = (
                db.query(Location, Location.coordinate.ST_AsText())
                .filter(Location.id == request.id)
                .one()
            )
            # Rely on database to return text form of point to reduce overhead of conversion in app code
            location.wkt_shape = coord_text
            locationItem = location_pb2.LocationMessage(
                id=location.id,
                person_id=location.person_id,
                longitude=location.longitude,
                latitude=location.latitude,
                creation_time=location.creation_time.strftime(DATETIME_FORMAT)
            )
            logging.info("Retrieve location end")
            return locationItem
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def Create(self, request, context):
        logging.info("Create location start")
        print("Create location start")
        try:
            message = {
                "person_id": request.person_id,
                "longitude": request.longitude,
                "latitude": request.latitude,
                "creation_time": request.creation_time,
            }
            logging.info("Send message to kafka queue")
            print("Send message to kafka queue")
            data = json.dumps(message)
            logging.info("Queue message json: " + data)
            print("Queue message json: " + data)
            producer.send(config.LOCATION_TOPIC_NAME, data.encode('utf-8'))
            producer.flush()
            logging.info("Create location end")
            return location_pb2.Empty()
        except Exception as e:
            print(e)
            return None

# Init gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)

# Initialize DB
ENV = os.getenv("ENV", "test")
config = config_by_name[ENV]
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
db = scoped_session(sessionmaker(bind=engine))

# Initialize Kafka
producer = KafkaProducer(bootstrap_servers=config.KAFKA_SERVER, api_version=(0, 10, 1))

print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
