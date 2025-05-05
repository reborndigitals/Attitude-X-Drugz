from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls import filters as call_filters
from pytgcalls.types import ChatUpdate
import logging
import asyncio
from config import API_ID, API_HASH, STRING_SESSION
from tools import end, hd_stream_closed_kicked

# Initialize logger
logger = logging.getLogger(__name__)


session = Client(
        "session",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION,
        in_memory=True,
        no_updates=True,
        sleep_threshold=32
    )
call_py = PyTgCalls(session)
    # Add handlers
call_py.add_handler(end, call_filters.stream_end())
call_py.add_handler(hd_stream_closed_kicked,
        call_filters.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT) |
        call_filters.chat_update(ChatUpdate.Status.KICKED)
    )
    
async def main():
    # Session client

    # Start both clients
    await call_py.start()
    
    logger.info("Joining required channels...")
    try:
        await session.join_chat("sheepra_cutie")
        await session.join_chat("nub_coder_s")
        await session.join_chat("nub_coder_updates")
        logger.info("Successfully joined all required channels")
    except Exception as e:
        logger.error(f"Error joining channels: {e}")

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
