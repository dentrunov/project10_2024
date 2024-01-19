from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.types import  KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header

from config import *

class OrderActions(StatesGroup):
    name_user = State()
    problem_user = State()

bot = Bot(token=TOKEN)
dp = Dispatcher()

button_start = KeyboardButton(text='Вернуться в начало')
# button_1 = KeyboardButton(text='Решение проблем')
button_2 = KeyboardButton(text='Сообщение администратору')
# keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2]], resize_keyboard=True)
keyboard = ReplyKeyboardMarkup(keyboard=[[button_2], [button_start]], resize_keyboard=True)

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer("""Здравствуйте!
Это бот технической поддержки электронного журнала!
Нажмите "Сообщение администратору", если вы хотите оставить сообщение""", reply_markup=keyboard)

@dp.message(F.text.lower() == "вернуться в начало")
async def process_start_command(message: Message):
    await message.answer("""Здравствуйте!
Это бот технической поддержки электронного журнала!
Нажмите "Сообщение администратору", если вы хотите оставить сообщение""", reply_markup=keyboard)

@dp.message(F.text.lower() == "сообщение администратору")
async def send_name(message: Message, state: FSMContext):
    await state.set_state(OrderActions.name_user)
    await message.reply(text="Представьтесь", reply_markup=ReplyKeyboardRemove())

@dp.message(StateFilter("OrderActions:name_user"))
async def send_problem(message: Message, state: FSMContext):
    await state.update_data(name_user=message.text.lower())
    await state.set_state(OrderActions.problem_user)
    await message.reply(text="Опишите проблему", reply_markup=ReplyKeyboardRemove())

@dp.message(StateFilter("OrderActions:problem_user"))
async def send_problem(message: Message, state: FSMContext):
    await state.update_data(problem_user=message.text.lower())
    data = await state.get_data()
    name_user = data["name_user"]
    problem_user = data["problem_user"]

    await send_mail(data, name_user, problem_user)
    await state.clear()
    await message.reply(text=f"Спасибо за сообщение, {name_user}!")
    await message.reply(text=f"Ваше сообщение отправлено:\nЕго содержание:\n{problem_user}", reply_markup=keyboard)

async def send_mail(data, name_user, problem_user):
    server = SMTP(smtp_server, port)
    server.starttls()  # обновляем соединение с использованием TLS-шифрования
    server.login(from_email, password)
    message = problem_user
    print(data)
    mime = MIMEText(message)
    mime['Subject'] = Header(f"{subject} от {name_user}", 'utf-8')

    server.sendmail(from_email, to_email, mime.as_string())
    server.quit()
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)

if __name__ == '__main__':
    dp.run_polling(bot)