# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connection.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x63onnection.proto\"v\n\x19LocationConnectionMessage\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x11\n\tperson_id\x18\x02 \x01(\x03\x12\x11\n\tlongitude\x18\x03 \x01(\t\x12\x10\n\x08latitude\x18\x04 \x01(\t\x12\x15\n\rcreation_time\x18\x05 \x01(\x03\"b\n\x17PersonConnectionMessage\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\x14\n\x0c\x63ompany_name\x18\x04 \x01(\t\"k\n\x11\x43onnectionMessage\x12,\n\x08location\x18\x01 \x01(\x0b\x32\x1a.LocationConnectionMessage\x12(\n\x06person\x18\x02 \x01(\x0b\x32\x18.PersonConnectionMessage\"_\n\x14GetConnectionRequest\x12\x11\n\tperson_id\x18\x01 \x01(\x03\x12\x12\n\nstart_date\x18\x02 \x01(\t\x12\x10\n\x08\x65nd_date\x18\x03 \x01(\t\x12\x0e\n\x06meters\x18\x04 \x01(\x05\"@\n\x15\x43onnectionMessageList\x12\'\n\x0b\x63onnections\x18\x01 \x03(\x0b\x32\x12.ConnectionMessage2S\n\x11\x43onnectionService\x12>\n\rFind_Contacts\x12\x15.GetConnectionRequest\x1a\x16.ConnectionMessageListb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'connection_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LOCATIONCONNECTIONMESSAGE._serialized_start=20
  _LOCATIONCONNECTIONMESSAGE._serialized_end=138
  _PERSONCONNECTIONMESSAGE._serialized_start=140
  _PERSONCONNECTIONMESSAGE._serialized_end=238
  _CONNECTIONMESSAGE._serialized_start=240
  _CONNECTIONMESSAGE._serialized_end=347
  _GETCONNECTIONREQUEST._serialized_start=349
  _GETCONNECTIONREQUEST._serialized_end=444
  _CONNECTIONMESSAGELIST._serialized_start=446
  _CONNECTIONMESSAGELIST._serialized_end=510
  _CONNECTIONSERVICE._serialized_start=512
  _CONNECTIONSERVICE._serialized_end=595
# @@protoc_insertion_point(module_scope)
