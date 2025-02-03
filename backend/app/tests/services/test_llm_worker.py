# tests/test_llm_worker.py

import asyncio
import time

import pytest
from app.services.llm_worker import LLMWorker

@pytest.mark.asyncio
async def test_run_inference_simple():
    """
    Test that a simple synchronous function can be offloaded
    to the worker and return the correct result.
    """
    worker = LLMWorker(max_workers=1)

    def add(a, b):
        return a + b

    result = await worker.run_inference(add, 2, 3)
    assert result == 5, f"Expected 5, got {result}"

    worker.shutdown()


@pytest.mark.asyncio
async def test_run_inference_concurrency():
    """
    Test concurrency by running two slow tasks in parallel.
    With max_workers=2, we expect both tasks to complete in ~1 second,
    rather than ~2 seconds if run sequentially.
    """
    worker = LLMWorker(max_workers=2)

    def slow_function(x):
        time.sleep(1)
        return x * x

    start_time = time.time()

    tasks = [
        asyncio.create_task(worker.run_inference(slow_function, 2)),
        asyncio.create_task(worker.run_inference(slow_function, 3))
    ]

    results = await asyncio.gather(*tasks)
    end_time = time.time()

    # We expect the results to match [4, 9]
    assert results == [4, 9], f"Expected [4, 9], got {results}"

    # Check if the total time is less than 2 seconds to confirm parallel execution
    elapsed = end_time - start_time
    assert elapsed < 2.0, f"Expected concurrency to finish under 2s; took {elapsed:.2f}s"

    worker.shutdown()


@pytest.mark.asyncio
async def test_run_inference_exceptions():
    """
    Test that if the offloaded function raises an exception,
    it propagates to the caller.
    """
    worker = LLMWorker(max_workers=1)

    def error_function():
        raise ValueError("Test error")

    with pytest.raises(ValueError) as exc_info:
        await worker.run_inference(error_function)

    # Confirm that the exception message is propagated
    assert "Test error" in str(exc_info.value)

    worker.shutdown()


@pytest.mark.asyncio
async def test_worker_shutdown_multiple_times():
    """
    Test that shutting down multiple times doesn't raise errors.
    This verifies idempotency and ensures no side effects.
    """
    worker = LLMWorker(max_workers=1)

    # Run a trivial function to show the worker is alive
    def identity(x):
        return x

    result = await worker.run_inference(identity, 10)
    assert result == 10

    # Shutdown the first time
    worker.shutdown()

    # Shutting down again should not raise exceptions
    worker.shutdown()