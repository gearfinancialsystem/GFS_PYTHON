import asyncio
import logging
from typing import AsyncIterator, List, Optional
import grpc
from grpc import aio

from .grpc_gen import helloworld_pb2, helloworld_pb2_grpc

logger = logging.getLogger(__name__)


class AsyncGrpcClient:
    """
    Asynchronous gRPC client for handling both unary and streaming responses.
    """

    def __init__(self, host: str = 'localhost', port: int = 50051):
        self.server_address = f"{host}:{port}"
        self.channel = None
        self.stub = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        """Establish connection to gRPC server"""
        try:
            self.channel = aio.insecure_channel(self.server_address)
            self.stub = helloworld_pb2_grpc.GreeterStub(self.channel)
            logger.info(f"Connected to gRPC server at {self.server_address}")
        except Exception as e:
            logger.error(f"Failed to connect to gRPC server: {e}")
            raise

    async def close(self):
        """Close the gRPC connection"""
        if self.channel:
            await self.channel.close()
            logger.info("gRPC connection closed")

    async def say_hello(self, name: str) -> str:
        """
        Send a unary request and get a single response.

        Args:
            name: Name to send in the request

        Returns:
            Single message from the server
        """
        if not self.stub:
            await self.connect()

        request = helloworld_pb2.HelloRequest(name=name)

        try:
            response = await self.stub.SayHello(request)
            return response.message
        except grpc.aio.AioRpcError as e:
            logger.error(f"gRPC error: {e.code()}, details: {e.details()}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    async def say_hello_stream(self, name: str) -> AsyncIterator[str]:
        """
        Send a request and receive streaming responses.

        Args:
            name: Name to send in the request

        Yields:
            String messages from the server
        """
        if not self.stub:
            await self.connect()

        request = helloworld_pb2.HelloRequest(name=name)

        try:
            async for response in self.stub.SayHelloStream(request):
                yield response.message
        except grpc.aio.AioRpcError as e:
            logger.error(f"gRPC error: {e.code()}, details: {e.details()}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    async def collect_all_stream_messages(self, name: str) -> List[str]:
        """
        Collect all streaming messages into a list.

        Args:
            name: Name to send in the request

        Returns:
            List of all messages received from the stream
        """
        messages = []
        async for message in self.say_hello_stream(name):
            messages.append(message)
        return messages


class StreamManager:
    """
    Higher-level manager for handling gRPC streams with callbacks.
    """

    def __init__(self, client: AsyncGrpcClient):
        self.client = client
        self._is_running = False

    async def start_stream_with_callback(self, name: str, callback=None):
        """
        Start streaming with optional callback for each message.

        Args:
            name: Name to send in the request
            callback: Async function to call for each message
        """
        self._is_running = True

        try:
            async for message in self.client.say_hello_stream(name):
                if not self._is_running:
                    break

                if callback:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(message)
                    else:
                        callback(message)
        except Exception as e:
            logger.error(f"Error in stream: {e}")
        finally:
            self._is_running = False

    def stop_stream(self):
        """Stop the ongoing stream"""
        self._is_running = False


# Convenience functions
async def create_client(host: str = 'localhost', port: int = 50051) -> AsyncGrpcClient:
    """Factory function to create and connect a client"""
    client = AsyncGrpcClient(host, port)
    await client.connect()
    return client