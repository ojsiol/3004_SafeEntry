# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: safeentry.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fsafeentry.proto\x12\tsafeentry\"W\n\x07Request\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04NRIC\x18\x02 \x01(\t\x12\x10\n\x08location\x18\x03 \x01(\t\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x10\n\x08\x64\x61tetime\x18\x05 \x01(\t\"\x18\n\x05Reply\x12\x0f\n\x07message\x18\x01 \x01(\t2\xab\x01\n\tSafeEntry\x12\x31\n\x07\x43heckin\x12\x12.safeentry.Request\x1a\x10.safeentry.Reply\"\x00\x12\x38\n\x0cGroupCheckin\x12\x12.safeentry.Request\x1a\x10.safeentry.Reply\"\x00(\x01\x12\x31\n\x07History\x12\x12.safeentry.Request\x1a\x10.safeentry.Reply\"\x00\x62\x06proto3')



_REQUEST = DESCRIPTOR.message_types_by_name['Request']
_REPLY = DESCRIPTOR.message_types_by_name['Reply']
Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'safeentry_pb2'
  # @@protoc_insertion_point(class_scope:safeentry.Request)
  })
_sym_db.RegisterMessage(Request)

Reply = _reflection.GeneratedProtocolMessageType('Reply', (_message.Message,), {
  'DESCRIPTOR' : _REPLY,
  '__module__' : 'safeentry_pb2'
  # @@protoc_insertion_point(class_scope:safeentry.Reply)
  })
_sym_db.RegisterMessage(Reply)

_SAFEENTRY = DESCRIPTOR.services_by_name['SafeEntry']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST._serialized_start=30
  _REQUEST._serialized_end=117
  _REPLY._serialized_start=119
  _REPLY._serialized_end=143
  _SAFEENTRY._serialized_start=146
  _SAFEENTRY._serialized_end=317
# @@protoc_insertion_point(module_scope)
