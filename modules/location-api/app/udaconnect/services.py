import logging
import grpc
import sys
import os
sys.path.append(os.path.abspath('../../../..'))

from datetime import datetime, timedelta
from typing import Dict, List
from app import db
from common.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

import common.proto.location_pb2 as location_pb2
import common.proto.location_pb2_grpc as location_pb2_grpc

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location-api")

locationChannel = grpc.insecure_channel("localhost:5005")
locationStub = location_pb2_grpc.LocationServiceStub(locationChannel)

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        response = locationStub.Retrieve(location_pb2.RetrieveLocationRequest(id=int(location_id)))
        location=Location(
                id=response.id,
                person_id=response.person_id,
                creation_time=datetime.fromtimestamp(response.creation_time),
            )
        location.set_wkt_with_coords(response.latitude, response.longitude)
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        response = locationStub.Create(location_pb2.LocationMessage(
            person_id=int(location["person_id"]),
            longitude=location["longitude"],
            latitude=location["latitude"],
            creation_time= int(datetime.strptime(location["creation_time"], DATETIME_FORMAT).timestamp())
        ))
        return response