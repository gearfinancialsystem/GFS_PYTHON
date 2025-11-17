import asyncio
import logging
from typing import List, Callable, Any, Dict
from .client import AsyncGrpcClient


def setup_logging(level=logging.INFO):
    """Setup basic logging configuration"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


async def process_stream_batch(names: List[str],
                               host: str = 'localhost',
                               port: int = 50051) -> Dict[str, List[str]]:
    """
    Process multiple stream requests in batch.

    Args:
        names: List of names to process
        host: gRPC server host
        port: gRPC server port

    Returns:
        Dictionary mapping names to their message lists
    """
    results = {}

    async with AsyncGrpcClient(host, port) as client:
        tasks = []
        for name in names:
            task = client.collect_all_stream_messages(name)
            tasks.append(task)

        # Process all requests concurrently
        gathered_results = await asyncio.gather(*tasks, return_exceptions=True)

        for name, result in zip(names, gathered_results):
            if isinstance(result, Exception):
                results[name] = [f"Error: {result}"]
            else:
                results[name] = result

    return results


async def process_unary_batch(names: List[str],
                              host: str = 'localhost',
                              port: int = 50051) -> Dict[str, str]:
    """
    Process multiple unary requests in batch.

    Args:
        names: List of names to process
        host: gRPC server host
        port: gRPC server port

    Returns:
        Dictionary mapping names to their responses
    """
    results = {}

    async with AsyncGrpcClient(host, port) as client:
        tasks = []
        for name in names:
            task = client.say_hello(name)
            tasks.append(task)

        # Process all requests concurrently
        gathered_results = await asyncio.gather(*tasks, return_exceptions=True)

        for name, result in zip(names, gathered_results):
            if isinstance(result, Exception):
                results[name] = f"Error: {result}"
            else:
                results[name] = result

    return results