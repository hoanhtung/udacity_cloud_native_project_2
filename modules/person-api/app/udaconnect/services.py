import logging
import grpc
import sys
import os
sys.path.append(os.path.abspath('../../../..'))

from datetime import datetime, timedelta
from typing import Dict, List
from app import db
from common.models import Person
from app.udaconnect.schemas import PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-person-api")

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()
