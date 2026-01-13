import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiohttp import web

# SIZNING BOT TOKENINGIZ
TOKEN = "8513575851:AAE40PrEkbs8cwijIKo9OmsvdBGHOv-zLts"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Har bir foydalanuvchi uchun alohida jarayonlarni boshqarish
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
            try:
                await task
            except asyncio.CancelledError:
                pass
        del user_tasks[user_id]

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await cancel_user_task(message.from_user.id)
    welcome_text = (
        "Xolisxon ❤️\n"
        "Bu bot sevgi va extiros bilan ishlaydi.\n"
        "Istalgan payt STOP bosib to‘xtatishing mumkin ⛔"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

async def infinite_loop_handler(message: types.Message, phrases: list):
    msg = await message.answer(random.choice(phrases))
    try:
        while True:
            await asyncio.sleep(random.uniform(0.3, 0.5))
            new_phrase = random.choice(phrases)
            if msg.text != new_phrase:
                await msg.edit_text(new_phrase)
    except asyncio.CancelledError:
        raise

@dp.message(F.text == "♾ Cheksiz Sevgi Oqimi")
async def love_stream(message: types.Message):
    await cancel_user_task(message.from_user.id)
    phrases = ["Seni sevaman ❤️", "Seni juda ko‘p sevaman 💋", "Sen mening hamma narsamsan 🔥", "Sensiz yashay olmayman…"]
    user_tasks[message.from_user.id] = asyncio.create_task(infinite_loop_handler(message, phrases))

@dp.message(F.text == "♾ Cheksiz Extiros")
async def passion_stream(message: types.Message):
    await cancel_user_task(message.from_user.id)
    phrases = ["Extirosli tun 🔥", "Vujudim yonmoqda... 💋", "Sog'inchim cheksiz...", "Yoningda bo'lishni xohlayman!"]
    user_tasks[message.from_user.id] = asyncio.create_task(infinite_loop_handler(message, phrases))

@dp.message(F.text == "⛔ STOP")
async def stop_action(message: types.Message):
    await cancel_user_task(message.from_user.id)
    await message.answer("To‘xtadi ❤️", reply_markup=get_main_keyboard())

@dp.message(F.text == "🎶 Qo‘shiqlar")
async def songs_handler(message: types.Message):
    await cancel_user_task(message.from_user.id)
    songs = ["🎵 Sevgi taronasi", "🎵 Yurak urishi", "🎵 Mayin ovoz..."]
    await message.answer(f"Siz uchun maxsus: {random.choice(songs)} ❤️")

@dp.message(F.text == "📝 She’rlar")
async def poems_handler(message: types.Message):
    await cancel_user_task(message.from_user.id)
    poems = ["Seni ko'rib ko'zim quvnar...", "Ishqingda yondi bu dil...", "Sen mening orzuyimdagisan..."]
    await message.answer(f"Sizga atalgan she'r: \n\n{random.choice(poems)} 📝")

@dp.message(F.text.in_({"🔥 Yurakni Erit", "🌙 Tungi Vasvasa", "🎭 Sirli Iqror"}))
async def other_features(message: types.Message):
    await cancel_user_task(message.from_user.id)
    await message.answer(f"{message.text} bo'limi faollashdi. ✨")

# --- KOYEB SERVERI UCHUN MUHIM QISM ---
async def main():
    # 1. Botni ishga tushirish
    asyncio.create_task(dp.start_polling(bot))

    # 2. Koyeb kutayotgan 8000-portda soxta server yoqish
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    
    # Bot o'chib qolmasligi uchun kutish
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
