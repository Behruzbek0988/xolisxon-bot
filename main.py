import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiohttp import web

# TOKEN
TOKEN = "8513575851:AAE40PrEkbs8cwijIKo9OmsvdBGHOv-zLts"

bot = Bot(token=TOKEN)
dp = Dispatcher()
user_tasks = {}

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="♾ Cheksiz Sevgi Oqimi"), types.KeyboardButton(text="♾ Cheksiz Extiros"))
    builder.row(types.KeyboardButton(text="🎶 Qo‘shiqlar"), types.KeyboardButton(text="📝 She’rlar"))
    builder.row(types.KeyboardButton(text="🔥 Yurakni Erit"), types.KeyboardButton(text="🌙 Tungi Vasvasa"))
    builder.row(types.KeyboardButton(text="🎭 Sirli Iqror"))
    builder.row(types.KeyboardButton(text="⛔ STOP"))
    return builder.as_markup(resize_keyboard=True)

async def cancel_user_task(user_id):
    if user_id in user_tasks:
        task = user_tasks[user_id]
        if not task.done():
            task.cancel()
        del user_tasks[user_id]

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await cancel_user_task(message.from_user.id)
    await message.answer("Xolisxon ❤️\nBot noldan ishga tushdi!", reply_markup=get_main_keyboard())

async def infinite_loop_handler(message: types.Message, phrases: list):
    msg = await message.answer(random.choice(phrases))
    try:
        while True:
            await asyncio.sleep(0.4)
            new_text = random.choice(phrases)
            await msg.edit_text(new_text)
    except Exception:
        pass

@dp.message(F.text == "♾ Cheksiz Sevgi Oqimi")
async def love_stream(message: types.Message):
    await cancel_user_task(message.from_user.id)
    phrases = ["Seni sevaman ❤️", "Sog'indim 💋", "Sensiz yasholmayman 🔥", "Yuragim seniki! ✨"]
    user_tasks[message.from_user.id] = asyncio.create_task(infinite_loop_handler(message, phrases))

@dp.message(F.text == "♾ Cheksiz Extiros")
async def passion_stream(message: types.Message):
    await cancel_user_task(message.from_user.id)
    phrases = ["Extirosli tun 🔥", "Vujudim yonmoqda... 💋", "Seni xohlayman! ✨"]
    user_tasks[message.from_user.id] = asyncio.create_task(infinite_loop_handler(message, phrases))

@dp.message(F.text == "⛔ STOP")
async def stop_action(message: types.Message):
    await cancel_user_task(message.from_user.id)
    await message.answer("To‘xtadi ❤️", reply_markup=get_main_keyboard())

# Qo'shimcha bo'limlar uchun oddiy javoblar
@dp.message(F.text.in_({"🎶 Qo‘shiqlar", "📝 She’rlar", "🔥 Yurakni Erit", "🌙 Tungi Vasvasa", "🎭 Sirli Iqror"}))
async def other_sections(message: types.Message):
    await cancel_user_task(message.from_user.id)
    await message.answer(f"{message.text} bo'limi tez kunda boyitiladi! ❤️")

async def main():
    asyncio.create_task(dp.start_polling(bot))
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 8000).start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
