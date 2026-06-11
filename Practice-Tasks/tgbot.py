import asyncio
import logging
import random
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- Конфигурация ---
API_TOKEN = '8751949359:AAGr9PtYaKkRsZehsWZp9Z9sCD39FzXZaTw'
WEATHER_API_KEY = '74adb9ce499a882ba99b4e427f242914'  # Опционально для /weather

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- Состояния (FSM) ---
class Form(StatesGroup):
    waiting_for_number = State()  # Для проверки четности
    playing_game = State()       # Для мини-игры

# --- Клавиатуры ---
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/weather Астана"), KeyboardButton(text="/fact")],
        [KeyboardButton(text="/calc 5+5"), KeyboardButton(text="/game")]
    ],
    resize_keyboard=True
)

# --- ЧАСТЬ 1: Базовые команды ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Я твой многофункциональный помощник.", reply_markup=main_menu)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "/start - Запуск\n/about - О боте\n"
        "/calc [выражение] - Калькулятор\n/weather [город] - Погода\n"
        "/fact - Случайный факт\n/check - Проверка числа (FSM)"
    )
    await message.answer(help_text)

@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    await message.answer("Этот бот разработан в рамках учебного проекта. Версия 1.0.")

# --- ЧАСТЬ 2: Логика и FSM ---

@dp.message(Command("check"))
async def cmd_check(message: types.Message, state: FSMContext):
    await message.answer("Введите любое целое число:")
    await state.set_state(Form.waiting_for_number)

@dp.message(Form.waiting_for_number)
async def process_number(message: types.Message, state: FSMContext):
    if message.text.isdigit() or (message.text.startswith('-') and message.text[1:].isdigit()):
        num = int(message.text)
        parity = "четное" if num % 2 == 0 else "нечетное"
        sign = "положительное" if num > 0 else "отрицательное" if num < 0 else "ноль"
        
        await message.answer(f"Число {num}: {parity} и {sign}.")
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите именно число.")

@dp.message(Command("calc"))
async def cmd_calc(message: types.Message):
    try:
        expr = message.text.replace("/calc ", "").strip()
        # Безопасное вычисление только простых операций
        result = eval(expr, {"__builtins__": None}, {})
        await message.answer(f"Результат: {result}")
    except Exception:
        await message.answer("Ошибка! Используйте формат: /calc 2+2")

# --- ЧАСТЬ 3: Внешние API ---

@dp.message(Command("fact"))
async def cmd_fact(message: types.Message):
    response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    if response.status_code == 200:
        fact = response.json().get("text")
        await message.answer(f"Интересный факт: {fact}")

@dp.message(Command("weather"))
async def cmd_weather(message: types.Message):
    city = message.text.replace("/weather ", "").strip()
    if not city or city == "/weather":
        await message.answer("Введите город: /weather Астана")
        return
    
    # Пример запроса (требуется ключ OpenWeatherMap)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    res = requests.get(url).json()
    
    if res.get("cod") == 200:
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        await message.answer(f"В городе {city} сейчас {temp}°C, {desc}.")
    else:
        await message.answer("Город не найден.")

# --- РАСШИРЕНИЕ: Мини-игра ---

@dp.message(Command("game"))
async def cmd_game(message: types.Message, state: FSMContext):
    number = random.randint(1, 10)
    await state.update_data(secret_number=number)
    await message.answer("Я загадал число от 1 до 10. Угадай!")
    await state.set_state(Form.playing_game)

@dp.message(Form.playing_game)
async def play_game(message: types.Message, state: FSMContext):
    data = await state.get_data()
    secret = data.get("secret_number")
    
    if message.text.isdigit() and int(message.text) == secret:
        await message.answer("🎉 Угадал! Победа!")
        await state.clear()
    else:
        await message.answer("Неверно, попробуй еще раз или напиши /stop")

# --- Обработка текста и ошибок ---

@dp.message(F.text.lower() == "привет")
async def text_greet(message: types.Message):
    await message.answer("И тебе привет! Чем могу помочь?")

@dp.message()
async def unknown_command(message: types.Message):
    await message.answer("Я не понимаю эту команду. Воспользуйтесь /help.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
