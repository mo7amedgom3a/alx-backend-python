#!/usr/bin/env python3
"""Asynchronous coroutine that takes in an integer argument"""

import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """Asynchronous coroutine that takes in an integer argument"""
    import random
    delay = random.uniform(0.0, max_delay)
    await asyncio.sleep(delay)
    return delay
