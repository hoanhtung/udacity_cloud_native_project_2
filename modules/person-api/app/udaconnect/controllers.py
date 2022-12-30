from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath('../../../..'))

from common.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app.udaconnect.services import ConnectionService, LocationService, PersonService
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


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    @api.param("payload", "Person payload", _in="body", example={"first_name": "Uda", "last_name": "Connect", "company_name": "UdaConnect Company"})
    def post(self) -> Person:
        try:
            payload = request.get_json()
            new_person: Person = PersonService.create(payload)
            return new_person
        except Exception as e:
            return handle_exception(e)

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        try:
            person: Person = PersonService.retrieve(person_id)
            return person
        except Exception as e:
            return handle_exception(e)


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        try:
            start_date: datetime = datetime.strptime(request.args["start_date"], DATE_FORMAT)
            end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
            distance: Optional[int] = request.args.get("distance", 5)

            results = ConnectionService.find_contacts(
                person_id=person_id,
                start_date=start_date,
                end_date=end_date,
                meters=distance,
            )
            return results
        except Exception as e:
            return handle_exception(e)