# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import safeentry_pb2 as safeentry__pb2


class SafeEntryStub(object):
    """The greeting service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Checkin = channel.unary_unary(
                '/safeentry.SafeEntry/Checkin',
                request_serializer=safeentry__pb2.Request.SerializeToString,
                response_deserializer=safeentry__pb2.Reply.FromString,
                )
        self.History = channel.unary_unary(
                '/safeentry.SafeEntry/History',
                request_serializer=safeentry__pb2.Request.SerializeToString,
                response_deserializer=safeentry__pb2.Reply.FromString,
                )


class SafeEntryServicer(object):
    """The greeting service definition.
    """

    def Checkin(self, request, context):
        """rpc Add (Request) returns (Reply) {}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def History(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SafeEntryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Checkin': grpc.unary_unary_rpc_method_handler(
                    servicer.Checkin,
                    request_deserializer=safeentry__pb2.Request.FromString,
                    response_serializer=safeentry__pb2.Reply.SerializeToString,
            ),
            'History': grpc.unary_unary_rpc_method_handler(
                    servicer.History,
                    request_deserializer=safeentry__pb2.Request.FromString,
                    response_serializer=safeentry__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'safeentry.SafeEntry', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SafeEntry(object):
    """The greeting service definition.
    """

    @staticmethod
    def Checkin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/safeentry.SafeEntry/Checkin',
            safeentry__pb2.Request.SerializeToString,
            safeentry__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def History(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/safeentry.SafeEntry/History',
            safeentry__pb2.Request.SerializeToString,
            safeentry__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
