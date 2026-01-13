# Xolisxon Bot - FINAL PROFESSIONAL VERSION
import asyncio
import random
import logging
import sys
import os
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest

TOKEN = 8306323272:AAGoM3woo5q352gl0S5eNkuK4deDK0Jta1I

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
bot = Bot(token=TOKEN)
dp = Dispatcher()
active_tasks = {}

def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="♾ Cheksiz Sevgi Oqimi", callback_data="loop_love"),
         InlineKeyboardButton(text="♾ Cheksiz Extiros", callback_data="loop_passion")],
        [InlineKeyboardButton(text="🎶 Qo‘shiqlar (Qidirish)", callback_data="menu_songs"),
         InlineKeyboardButton(text="📝 She’rlar", callback_data="menu_poems")],
        [InlineKeyboardButton(text="🔥 Yurakni Erit", callback_data="mode_melt"),
         InlineKeyboardButton(text="🌙 Tungi Vasvasa", callback_data="mode_night")],
        [InlineKeyboardButton(text="🎭 Sirli Iqror", callback_data="mode_secret")],
        [InlineKeyboardButton(text="⛔ STOP", callback_data="stop_all")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Matnlar bazasi
LOVE_FLOW = ["Seni sevaman ❤️", "Yuragim faqat sen deb uradi 💓", "Sensiz yashay olmayman... ✨", "Sen mening dunyoyimsan 🌍", "Har nafasimda sening isming 🌬️", "Seni o'ylash - mening eng katta quvonchim 🥰", "Mening shirin hayotim - bu SEN 💋"]
PASSION_FLOW = ["Lablaring bolidan totgim kelyapti... 🍓", "Seni qattiq quchoqlasam deyman 💋", "Tunlari sening xayoling bilan yashayman 🌙", "Sog'indim... 🔥", "Vujudingni yaqinroq his qilishni xohlayman... ✨"]
POEMS = ["📝 Sening ishqingda ado bo'laman...", "📝 Muhabbat bog'ida ochilgan gulsiz...", "📝 Közlaringga termulib to'ymayman...", "📝 Ismingni takrorlab o'tadi kunlar...", "📝 Taqdirim sen bilan bog'langan ekan..."]
MELTING_TEXTS = ["🔥 Sening tabassuming dunyoni yoritadi.", "🔥 Men uchun eng baxtli lahza — sening ovozing.", "🔥 Sening mehring quyoshdan issiq."]
NIGHT_TEXTS = ["🌙 Tun quyuqlashganda seni sog'inaman.", "🌙 Shirin tushlar ko'r, farishtam...", "🌙 Oy nurida sening yuzingni ko'raman."]

async def download_audio(query):
    file_id = f"music_{random.randint(1000, 9999)}"
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': file_id, 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}], 'default_search': 'ytsearch1', 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await asyncio.get_event_loop().run_in_executor(None, lambda: ydl.download([query]))
        return f"{file_id}.mp3"
    except: return None

async def cancel_user_task(user_id):
    if user_id in active_tasks:
        task = active_tasks[user_id]
        if not task.done(): task.cancel()
        del active_tasks[user_id]

async def run_loop(user_id, message_id, messages, mode_name):
    try:
        while True:
            text = random.choice(messages)
            try:
                await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                    text=f"❤️ **{mode_name}**\n\n{text}\n\n[Keyingi xabar 5-10 soniyada... ♾]",
                    reply_markup=get_main_keyboard(), parse_mode="Markdown")
            except: pass
            await asyncio.sleep(random.randint(5, 10))
    except asyncio.CancelledError: pass

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await cancel_user_task(message.from_user.id)
    await message.answer("Xolisxon ❤️\nBarcha tugmalar ishchi holatda! Musiqa nomini yozing 🎶", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "stop_all")
async def cb_stop(callback: CallbackQuery):
    await cancel_user_task(callback.from_user.id)
    await callback.message.edit_text("Hamma jarayonlar to‘xtadi ❤️", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "loop_love")
async def cb_love(callback: CallbackQuery):
    uid, mid = callback.from_user.id, callback.message.message_id
    await cancel_user_task(uid)
    msg = await callback.message.edit_text("♾ Cheksiz Sevgi Oqimi boshlanmoqda... ❤️")
    active_tasks[uid] = asyncio.create_task(run_loop(uid, msg.message_id, LOVE_FLOW, "Sevgi Oqimi"))

@dp.message(F.text)
async def handle_music(message: types.Message):
    if message.text.startswith('/'): return
    await cancel_user_task(message.from_user.id)
    st = await message.answer(f"🔎 **'{message.text}'** qidirilmoqda...")
    path = await download_audio(message.text)
    if path and os.path.exists(path):
        await message.answer_audio(FSInputFile(path), caption=f"'{message.text}'\nXolisxon Bot ❤️", reply_markup=get_main_keyboard())
        await st.delete()
        os.remove(path)
    else: await st.edit_text("❌ Qo'shiq topilmadi.")

@dp.callback_query(F.data.in_({"menu_songs", "menu_poems", "mode_melt", "mode_night", "mode_secret"}))
async def cb_others(callback: CallbackQuery):
    await cancel_user_task(callback.from_user.id)
    content = random.choice(POEMS + MELTING_TEXTS + NIGHT_TEXTS)
    await callback.message.edit_text(content, reply_markup=get_main_keyboard())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    if sys.platform == "win32": asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
