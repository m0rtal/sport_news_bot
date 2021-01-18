import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove
from nltk import sent_tokenize

from keyboards.default import startmenu
from loader import dp, db

from utils.get_gazzetta_posts import get_gazzetta_rss_links, get_gazzetta_news


# from utils.db_api.sqlite import *

# ответ с кнопками меню
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        db.add_user(message.from_user.id)
    except sqlite3.IntegrityError as err:
        print(err)
    await message.answer("\n".join([
        f"Привет, {message.from_user.full_name}!",
        f"Ты был занесён в базу пользователей",
        f"Всего пользователей: {db.count_users()}"
    ]), reply_markup=startmenu)


# Обработка нажатий на кнопку получения новостей
@dp.message_handler(text="Получить обновления новостей")
async def get_news(message: types.Message):
    await message.answer("Работаю, подождите...")
    all_posts = await get_gazzetta_rss_links()
    user_id = message.from_user.id
    sent_msgs = db.get_sent_messages(user_id)
    posts = [post for post in all_posts if
             "gazzetta" in post and "video" not in post and post not in sent_msgs]

    for post in posts:
        rawtext, translation = await get_gazzetta_news(post)
        if translation:
            await message.answer(post)
            if len(translation) <= 3500:
                await message.answer(translation, reply_markup=ReplyKeyboardRemove())
            else:
                fivek = ""
                for sentence in sent_tokenize(text=translation, language="russian"):
                    if len(fivek + sentence) < 3500:
                        fivek += sentence
                    else:
                        await message.answer(fivek)
                        fivek = sentence
                await message.answer(fivek, reply_markup=ReplyKeyboardRemove())

            if post not in db.gazzetta_posts_links():
                db.add_gazzetta_post(post, rawtext, translation)
        db.add_to_sent_messages(user_id, post)
    await message.answer("Нет больше постов", reply_markup=ReplyKeyboardRemove())
