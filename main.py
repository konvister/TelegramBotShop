from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import Config as conf
from db import Database

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('/help'))


bot = Bot(conf.TOKEN_API)
dp = Dispatcher(bot)
db = Database('TelegramBot.db')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        await message.answer(text=conf.START_COMMAND,
                             reply_markup=kb)
        await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=conf.HELP_COMMAND)
    await message.delete()


@dp.message_handler(commands=['sendall'])
async def sendall(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == conf.ADMIN_ID:
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)

            await bot.send_message(message.from_user.id, "Успешная рассылка")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
