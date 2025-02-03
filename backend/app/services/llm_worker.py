# app/clients/llm_worker.py

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any

class LLMWorker:
    """
    Manages a ThreadPoolExecutor for CPU-bound operations like
    running Hugging Face pipeline inference. 
    """

    def __init__(self, max_workers: int = 1):
        """
        Initialize the ThreadPoolExecutor. 
        max_workers=1 ensures only one pipeline inference at a time, 
        but you can increase it if you have enough CPU/GPU resources.
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def run_inference(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        """
        Schedules a CPU-bound function (`func`) to run in the thread pool, 
        returns the result asynchronously.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, func, *args, **kwargs)

    def shutdown(self):
        """
        Shutdown the executor properly.
        """
        self.executor.shutdown(wait=True)