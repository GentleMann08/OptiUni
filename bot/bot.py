import asyncio
import sqlite3

import pandas as pd
from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.types import CallbackQuery, Message
from aiogram.types import FSInputFile
from telethon.sync import TelegramClient

from olymps import get_olymps
import database
import parse
import structure


bot = Bot('Bot Token Here')
dp = Dispatcher()
admins = [1219940023, 1132908805]


def zagl(string):
    return string[0].upper() + string[1:]


def set_program_text(program):
    return f'📍 Появилась {structure.set_title(program["title"])}\n\n' \
           f'{structure.icons[program["subject"]][0]} Предмет - {program["subject"]}\n' \
           f'🎒 Для {program["class"]} классов\n' \
           f'🗓️ С{program["dates"][1:]}\n' \
           f'{structure.place_icons[program["place"]][0]} Место - {structure.place_icons[program["place"]][1]}\n\n' \
           f'❗ Регистрация до {program["register"]}'


def set_olymp_text(olymp):
    title = list(olymp['dates'].keys())[0]
    date = olymp['dates'][title].lower()
    temp = "\n".join([zagl(i) for i in olymp["subjects"]])
    if not 'до' in date:
        date = 'до ' + date
    return f'📍 Совсем скоро начнется {olymp["title"]}\n\n' \
           f'👀 Дисциплины: {temp}\n' \
           f'🎒 Для {olymp["classes"][0]}-{olymp["classes"][-1]} классов\n' \
           f'🏅 Место РЦОИ - {olymp["place"]}\n' \
           f'📶 Уровень - {olymp["level"]}\n' \
           f'❗ {zagl(title)} {date}'


async def program_loop():
    print('Начало рассылки программ')
    users = database.send_program()
    programs = parse.main()
    new = []
    for program in programs:
        for user in users[program['subject']]:
            try:
                await bot.send_photo(chat_id=user,
                                     photo=program['image'],
                                     caption=set_program_text(program),
                                     reply_markup=structure.set_url(program["url"]))
                print(f'[+] {program["title"]} отправлена в пользователю {user}')

                await asyncio.sleep(2.1)
            except:
                pass
        new.append(program['url'])
    database.new_urls(new)
    print('Рассылка программ завершена')
    await asyncio.sleep(21600)


async def olymp_loop():
    print('Начало рассылки олимпиад')
    users = database.send_olymp()
    olymps = get_olymps()
    for olymp in olymps:
        for subject in olymp['subjects']:
            if not zagl(subject) in structure.subjects:
                continue
            for user in users[zagl(subject)]:
                try:
                    await bot.send_message(chat_id=user,
                                           text=set_olymp_text(olymp),
                                           reply_markup=structure.set_url(olymp["url"]))
                    print(f'[+] {olymp["title"]} отправлена в пользователю {user}')

                    await asyncio.sleep(2.1)
                except:
                    pass
    print('Рассылка олимпиад завершена')
    await asyncio.sleep(86400)
    await olymp_loop()


async def start_bot():

    async with TelegramClient('Abdosha0', api_id, api_hash,
                              device_model="iPhone 13 Pro Max",
                              system_version="14.8.1",
                              app_version="8.4",
                              lang_code="en",
                              system_lang_code="en-US") as client:
        await client.send_message('more_vzlet_bot', '/start')
        await client.send_message('more_vzlet_bot', '/ol')


@dp.message(Command(commands=['log']))
async def log(message: Message):
    if message.from_user.id in admins:
        try:
            await message.answer_document(FSInputFile(path='/bot/nohup.out'))
        except:
            await message.answer('Файл пустой')
        df = pd.read_sql_query("SELECT * FROM user_info", sqlite3.connect('db.db'))
        df.to_excel('Пользователи.xlsx')
        df = pd.read_sql_query("SELECT * FROM sent", sqlite3.connect('db.db'))
        df.to_excel('Ссылки.xlsx')
        await message.answer_document(FSInputFile(path='/bot/База данных.xlsx'))
        await message.answer_document(FSInputFile(path='/bot/Ссылки.xlsx'))


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    print(message.from_user.username, message.from_user.id)
    if message.from_user.username == 'Abdosha0':
        await olymp_loop()
        return
    database.start_command(message.from_user.id)
    await message.answer(text='👋 Привет, подмосковный олимпиадник!\n\n'
                              'ℹ️ Я бот, для отслеживания появления новых смен в ОЦ Взлёт.\n',
                         reply_markup=structure.main_menu)
    await message.answer(
        text='⚙️ Давай включим нужные для тебя уведомления, ты сможешь изменить выбор в любой удобный момент! Выбери интересующую категорию',
        reply_markup=structure.set_middle_but('0', message.from_user.id))
    await asyncio.sleep(180)
    await message.answer(
        text='📍 Хотите ли вы получать уведомления о олимпиадах по вашим профилям?',
        reply_markup=structure.channel)


@dp.message(Text(text=['🔔 Настройка уведомлений']))
async def new_phone(message: Message):
    print(message.from_user.username, message.from_user.id, message.text)
    await message.answer(text='Выбери интересующую категорию',
                         reply_markup=structure.set_middle_but('0', message.from_user.id))


@dp.callback_query(Text(text=list(structure.graph.keys())))
async def cansel(callback: CallbackQuery):
    print(callback.from_user.username, callback.from_user.id, callback.data)
    await callback.message.edit_text(text='Выберите категорию',
                                     reply_markup=structure.set_middle_but(callback.data, callback.from_user.id))


@dp.callback_query(Text(text=structure.subjects))
async def cansel(callback: CallbackQuery):
    print(callback.from_user.username, callback.from_user.id, callback.data)
    await callback.message.edit_text(text='Выберите категорию',
                                     reply_markup=structure.set_notif(callback.from_user.id, callback.data))


@dp.callback_query(Text(text='olymp'))
async def cansel(callback: CallbackQuery):
    print(callback.from_user.username, callback.from_user.id, callback.data)
    database.set_olymp(callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=structure.set_middle_but('0', callback.from_user.id))


@dp.message(lambda message: message.from_user.id == message.chat.id)
async def message(message: Message):  #
    print(message.from_user.username, message.text)
    await message.answer('Неизвестная команда')


if __name__ == '__main__':
    # asyncio.run(start_bot())
    print('Бот запущен')
    dp.run_polling(bot)  # Запуск бота
