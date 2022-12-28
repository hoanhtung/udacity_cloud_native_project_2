import time
from concurrent import futures

import os
import sys
# Append parent directory to import path
sys.path.append(os.path.abspath('../../..'))

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

class LocationService(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):
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
                latitude=location.latitude,
                longitude=location.longitude,
                creation_time=int(location.creation_time.timestamp())
            )
                      
            return locationItem
        except Exception as e:
            print(e)
            db.rollback()
            return None

    def Create(self, request, context): 
        try:
            message = {
                'person_id': request.person_id,
                'creation_time': request.creation_time,
                'latitude': request.latitude,
                'longitude': request.longitude,
            }
            kafka_data = json.dumps(message).encode('utf-8')
            producer.send(config.LOCATION_TOPIC_NAME, kafka_data)
            producer.flush()
            
            return location_pb2.EmptyLocationResponse()
        except Exception as e:
            print(e)
            return None

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)

# Initialize DB
ENV = os.getenv("FLASK_ENV", "test")
config = config_by_name[ENV or "test"]
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
db = scoped_session(sessionmaker(bind=engine))

# Initialize Kafka
producer = KafkaProducer(bootstrap_servers=config.KAFKA_SERVER)

print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
