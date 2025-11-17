"""
Generated gRPC code from .proto files.
This module contains the auto-generated protobuf and gRPC classes.
"""

from . import helloworld_pb2
from . import helloworld_pb2_grpc

# Re-export the most commonly used classes for convenience
from .helloworld_pb2 import HelloRequest, HelloReply
from .helloworld_pb2_grpc import GreeterStub, GreeterServicer

__all__ = [
    'helloworld_pb2',
    'helloworld_pb2_grpc', 
    'HelloRequest',
    'HelloReply',
    'GreeterStub',
    'GreeterServicer',
]
