from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.types import  KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from smtplib import SMTP

from config import *

class OrderActions(StatesGroup):
    name_user = State()
    problem_user = State()

bot = Bot(token=TOKEN)
dp = Dispatcher()

button_1 = KeyboardButton(text='Проблема')
button_2 = KeyboardButton(text='Кнопка 2')
keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2]], resize_keyboard=True)

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь', reply_markup=keyboard)

@dp.message(F.text.lower() == "проблема")
async def send_name(message: Message, state: FSMContext):
    await state.set_state(OrderActions.name_user)
    await message.reply(text="Представьтесь")

@dp.message(StateFilter("OrderActions:name_user"))
async def send_problem(message: Message, state: FSMContext):
    await state.update_data(name_user=message.text.lower())
    await state.set_state(OrderActions.problem_user)
    await message.reply(text="Опишите проблему")

@dp.message(StateFilter("OrderActions:problem_user"))
async def send_problem(message: Message, state: FSMContext):
    await state.update_data(problem_user=message.text.lower())
    data = await state.get_data()
    name_user = data["name_user"]
    problem_user = data["problem_user"]

    # server = SMTP(smtp_server, port)
    # server.starttls()  # обновляем соединение с использованием TLS-шифрования
    # server.login(email, password)
    #
    # from_email = email
    # to_email = "recipient_email@example.com"
    # subject = "Тестовое сообщение"
    # message = "Привет, это тестовое сообщение, отправленное с помощью Python и SMTP."
    #
    # server.sendmail(from_email, to_email, f"Subject: {subject}\n\n{message}")

    await state.clear()
    await message.reply(text="Спасибо за сообщение!" +" " + name_user, reply_markup=keyboard)


@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)

if __name__ == '__main__':
    dp.run_polling(bot)