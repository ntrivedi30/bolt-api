import asyncio
from typing import Callable, List


class BackgroundTasks:
    def __init__(self):
        self.tasks: List[tuple[Callable, tuple, dict]] = []

    def add_task(self, func: Callable, *args, **kwargs):
        """
        Schedules a task to run after the response is sent.
        """
        self.tasks.append((func, args, kwargs))

    async def execute(self):
        """
        Runs all tasks. This is called by Bolt/Starlette internally.
        """
        for func, args, kwargs in self.tasks:
            if asyncio.iscoroutinefunction(func):
                await func(*args, **kwargs)
            else:
                # Run sync functions in a thread to avoid blocking the loop
                await asyncio.to_thread(func, *args, **kwargs)
