from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import pathlib
import config

cwd = pathlib.Path.cwd()
bot = Bot(token=config.token)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    print('start -----',str(message.chat.id))
    start_buttons = ['Добавить товар', 'Список товаров']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Меню', reply_markup=keyboard)


@dp.message_handler(Text(equals='Добавить товар'))
async def gen_frazu(message: types.Message):
    await message.answer('Добавляю товар')


@dp.message_handler(Text(equals='Список товаров'))
async def return_items(message: types.Message):
    await message.answer('Получаю список товаров')




def main():
    print('[INFO] TELEGRAMM BOT IS RUNNING')

    executor.start_polling(dp)


if __name__ == '__main__':
    main()
