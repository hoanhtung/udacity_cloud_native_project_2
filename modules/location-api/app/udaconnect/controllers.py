from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath('../../../..'))

from common.models import Connection, Location, Person
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling
def handle_exception(e):
    print(e)
    return Response("Whoops something went wrong on our servers!", status=500)

@api.route("/locations", methods=['POST'])
@api.route("/locations/<location_id>", methods=['GET'])
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        try:
            request.get_json()
            location: Location = LocationService.create(request.get_json())
            return location
        except Exception as e:
            return handle_exception(e)

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        try:
            location: Location = LocationService.retrieve(location_id)
            return location
        except Exception as e:
            return handle_exception(e)