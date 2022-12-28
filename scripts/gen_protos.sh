INCLUDE_LOCATION=./modules/common/proto
OUTPUT_LOCATION=./modules/common/proto
PROTO_FILE_LOCATION=location.proto
INCLUDE_CONNECTION=../modules/services/connection/proto
OUTPUT_CONNECTION=../modules/services/connection/proto
PROTO_FILE_CONNECTION=connection.proto
INCLUDE_PERSON=../modules/services/person/proto
OUTPUT_PERSON=../modules/services/person/proto
PROTO_FILE_PERSON=person.proto
#python -m grpc_tools.protoc -I$INCLUDE_CONNECTION --python_out=$OUTPUT_CONNECTION --grpc_python_out=$OUTPUT_CONNECTION $PROTO_FILE_CONNECTION
python -m grpc_tools.protoc -I$INCLUDE_LOCATION --python_out=$OUTPUT_LOCATION --grpc_python_out=$OUTPUT_LOCATION $PROTO_FILE_LOCATION
#python -m grpc_tools.protoc -I$INCLUDE_PERSON --python_out=$OUTPUT_PERSON --grpc_python_out=$OUTPUT_PERSON $PROTO_FILE_PERSON
