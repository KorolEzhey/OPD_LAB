import asyncio
import random
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command

async def main():
    bot = Bot(token="")
    dp = Dispatcher()
    r = Router()
    g = {}

    @r.message(Command(commands=["start", "help"]))
    async def cmd(message: types.Message):
        if message.text == "/start":
            await message.reply("Привет! Это бот 'Угадай число'. Используй /play!")
        elif message.text == "/help":
            await message.reply("Угадай число от 1 до 100!")

    @r.message()
    async def msg(message: types.Message):
        uid = message.from_user.id
        if message.text == "/play":
            g[uid] = random.randint(1, 10)
            await message.reply("Загадано число от 1 до 10. Назови вариант!")
        elif uid in g:
            try:
                n = int(message.text)
                if n == g[uid]:
                    await message.reply("Угадал! Начни заново с /play")
                    del g[uid]
                elif n < g[uid]:
                    await message.reply("Бери выше!")
                else:
                    await message.reply("Бери ниже!")
            except ValueError:
                await message.reply("Введи число!")
        else:
            await message.reply("Используй /play для начала!")

    dp.include_router(r)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())