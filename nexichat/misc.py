import time
import logging
import asyncio

from . import boot

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)


LOGGER = logging.getLogger(__name__)

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