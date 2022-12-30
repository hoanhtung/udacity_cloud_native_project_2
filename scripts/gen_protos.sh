INCLUDE_LOCATION=./modules/common/proto
OUTPUT_LOCATION=./modules/common/proto
PROTO_FILE_LOCATION=location.proto

python -m grpc_tools.protoc -I$INCLUDE_LOCATION --python_out=$OUTPUT_LOCATION --grpc_python_out=$OUTPUT_LOCATION $PROTO_FILE_LOCATION
