import time
from concurrent import futures

# import os
# import sys
# Append parent directory to import path
# sys.path.append(os.path.abspath('../../..'))

import grpc
import proto.person_pb2 as person_pb2
import proto.person_pb2_grpc as person_pb2_grpc
from common.models import Location
import json
from datetime import datetime
from common.config import config_by_name


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from geoalchemy2.functions import ST_AsText, ST_Point
from kafka import KafkaProducer

class PersonService(person_pb2_grpc.PersonServiceServicer):
    def Create(self, request, context):
        try:
            new_person = Person()
            new_person.first_name = request.first_name
            new_person.last_name = request.last_name
            new_person.company_name = request.company_name

            db.add(new_person)
            db.commit()

            personItem = person_pb2.PersonMessage(
                id=new_person.id,
                first_name=new_person.first_name,
                last_name=new_person.last_name,
                company_name=new_person.company_name
            )

            return personItem
        except Exception as e:
            print(e)
            db.rollback()
            return None

 def Retrieve(self, request, context):
        person = db.query(Person).get(request.id)
        personItem = person_pb2.PersonMessage(
            id=person.id,
            first_name=person.first_name,
            last_name=person.last_name,
            company_name=person.company_name
        )
        return personItem

    def RetrieveAll(self, request, context):
        persons = db.query(Person).all()
        result = person_pb2.PersonMessageList()
        for person in persons:
            personItem = person_pb2.PersonMessage(
                id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name
            )
            result.persons.extend([personItem])
        return result


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonService(), server)

# Initialize DB
ENV = os.getenv("FLASK_ENV", "test")
config = config_by_name[ENV or "test"]
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
db = scoped_session(sessionmaker(bind=engine))


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
