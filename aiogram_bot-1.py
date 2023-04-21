import logging

from aiogram import Bot, Dispatcher, executor, types

from Notion_logic import get_message

TELEGRAM_TOKEN

logging.basicConfig(level=logging.INFO)


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


def plus(a, b):
    return a + b


def menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_start = [types.InlineKeyboardButton(text="Все должники",
                                               callback_data="get_all"),
                    types.InlineKeyboardButton(text="Новые должники",
                                               callback_data="get_new"),
                    types.InlineKeyboardButton(text="Помощь",
                                               callback_data="get_help")]
    return keyboard.add(*button_start)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(
        message.chat.id, "Привет! Этот бот позволит тебе"
                         "получать списки должников."
                         " Выбери одну из опций, либо "
                         "введи /get_help для подробной справки.",
        reply_markup=menu())


@dp.message_handler(commands=['get_all'])
async def send_all(message: types.Message):
    for string in get_message()[0]:
        await message.reply(string)
    await bot.send_message(message.chat.id, "Опции", reply_markup=menu())


@dp.message_handler(commands=['get_new'])
async def send_new_info(message: types.Message):
    if len(get_message()[1]) == 0:
        await message.reply("Просрочивших выплату на один день должников нет")
    for string in get_message()[1]:
        await message.reply(string)
    await bot.send_message(message.chat.id, "Опции", reply_markup=menu())


@dp.message_handler(commands=['get_help'])
async def send_help(message: types.Message):
    await bot.send_message(message.chat.id,
                           text=("Это бот для выдачи списка должников."
                                 " Выбери одну из опций "
                                 "либо набери одну из комманд:\n"
                                 "/get_all - список всех должников,\n"
                                 "/get_new - список просрочивших "
                                 "выплату на один день должников,\n"
                                 "/get_help - для повтора справки."),
                           reply_markup=menu())


@dp.callback_query_handler(lambda call: call.data.split('_')[0] == 'get')
async def get_menu_press(callback: types.CallbackQuery):
    action = callback.data
    if action == "get_all":
        await send_all(callback.message)
    if action == "get_new":
        await send_new_info(callback.message)
    if action == "get_help":
        await send_help(callback.message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    print(plus(2, 2))
    print_hi('PyCharm')
