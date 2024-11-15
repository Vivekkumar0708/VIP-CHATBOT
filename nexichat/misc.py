import time
import asyncio

from . import boot


async def get_uptime():
    def _get_uptime():

        now_time = time.time()

        elapsed_time = now_time - boot
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        output = (
            (f"{hours} hrs " if hours > 0 else "") +
            (f"{minutes} minutes " if minutes > 0 else "") +
            f"{seconds} seconds"
        )

        return output.strip()
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _get_uptime)