"""
My gRPC Package - A Python package with async gRPC client capabilities.
"""

__version__ = "0.1.0"

from .client import AsyncGrpcClient, StreamManager, create_client
from .utils import setup_logging, process_stream_batch, process_unary_batch

__all__ = [
    "AsyncGrpcClient",
    "StreamManager",
    "create_client",
    "setup_logging",
    "process_stream_batch",
    "process_unary_batch",
]