import asyncio
from tg_bot.bot import start_bot
from actions import newsAddition, dataFromDatabase
if __name__ == "__main__":
    #asyncio.run(newsAddition(dataFromDatabase()))
    asyncio.run(start_bot())
    