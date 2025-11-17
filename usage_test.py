#!/usr/bin/env python3
"""
Example usage of the gRPC client package with helloworld proto.
"""
# %%
import asyncio
import logging
from pygfs import AsyncGrpcClient, StreamManager, create_client
# %%

async def example_unary_call():
    """Example of unary RPC call"""
    print("=== Unary RPC Example ===")

    async with AsyncGrpcClient('localhost', 50051) as client:
        response = await client.say_hello("Python User")
        print(f"Server response: {response}")


async def example_simple_stream():
    """Example of simple stream usage"""
    print("\n=== Simple Stream Example ===")

    async with AsyncGrpcClient('localhost', 50051) as client:
        print("Receiving stream messages...")
        async for message in client.say_hello_stream("Python User"):
            print(f"Received: {message}")


async def example_collect_all():
    """Example of collecting all stream messages"""
    print("\n=== Collect All Stream Messages Example ===")

    async with AsyncGrpcClient('localhost', 50051) as client:
        messages = await client.collect_all_stream_messages("Python User")
        print(f"All stream messages: {messages}")


async def example_with_callback():
    """Example using callback pattern for streams"""
    print("\n=== Stream Callback Example ===")

    def my_callback(message):
        print(f"Callback received: {message}")

    client = await create_client('localhost', 50051)
    manager = StreamManager(client)

    # Run for 10 seconds
    await asyncio.wait_for(
        manager.start_stream_with_callback("Python User", my_callback),
        timeout=10.0
    )


async def main():
    """Run all examples"""
    try:
        await example_unary_call()
        await example_simple_stream()
        await example_collect_all()
        await example_with_callback()
    except Exception as e:
        print(f"Example error: {e}")

# %%
# if __name__ == "__main__":
#     # Setup logging
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())

asyncio.run(example_unary_call())


