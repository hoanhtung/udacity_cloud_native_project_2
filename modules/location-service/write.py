import os
import sys
sys.path.append(os.path.abspath('../'))
import grpc
import logging
import common.proto.location_pb2 as location_pb2
import common.proto.location_pb2_grpc as location_pb2_grpc
# Run this code to make sample request

logging.basicConfig(level=logging.WARNING)
logging.info("Starting...")

try:
    channel = grpc.insecure_channel("localhost:5005")
    logging.info("Connected to localhost:5005")
    stub = location_pb2_grpc.LocationServiceStub(channel)

    # Update with your payload
    location = location_pb2.LocationMessage(
        id=10000,
        person_id=2,
        longitude="60.112244",
        latitude="-56.1231542",
        creation_time="2022-12-31T15:00:00"
    )
    print(location)
    response = stub.Create(location)
    logging.info(format(response))

except Exception as e:
    print(e)
    logging.error("Error occurs")