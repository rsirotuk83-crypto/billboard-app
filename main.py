import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Конфігурація
TOKEN = os.getenv("BOT_TOKEN")
app = FastAPI()
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Дозволяємо запити з GitHub Pages
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Імітація бази даних
state = {
    "vip_text": "Notcoin is the King! 🚀",
    "main_text": "Тут твоя реклама за 1 долар",
    "jackpot": 12.5,
    "last_vip_time": 0
}

@app.get("/status")
async def get_status():
    return state

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [[types.InlineKeyboardButton(text="🏙 Відкрити Білборд", web_app=types.WebAppInfo(url="https://yourname.github.io/billboard-app/"))]]
    await message.answer("🌆 Вітаємо! WBCB - це білборд, де ти можеш купити увагу всього TON.", 
                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    if message.web_app_data.data == "action:buy_stars":
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="Рекламне місце",
            description="Ваш текст на білборді на 10 хв",
            payload="stars_pay",
            provider_token="", # Для Stars порожньо
            currency="XTR",
            prices=[types.LabeledPrice(label="Billboard Slot", amount=50)]
        )

# Запуск
async def run_bot():
    await dp.start_polling(bot)

async def run_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_api())
    loop.run_until_complete(run_bot())
