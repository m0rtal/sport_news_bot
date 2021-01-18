from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import startmenu_cancel, startmenu
from loader import dp, db
from states import ValidTranslation


@dp.message_handler(text="Предложить свой перевод")
async def valid_translation(message: types.Message):
    await message.answer(
        "Пришлите ссылку на новость, перевод которой хотите предложить", reply_markup=startmenu_cancel)
    await ValidTranslation.link.set()


@dp.message_handler(text="Отмена", state=[ValidTranslation.link, ValidTranslation.translation])
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Приём перевода отменён", reply_markup=startmenu)
    await state.finish()


@dp.message_handler(state=ValidTranslation.link)
async def get_link_from_user(message: types.Message, state: FSMContext):
    link = message.text
    await state.update_data(post_link=link)
    await message.reply("Принял. Теперь пришлите корректный перевод.")
    await ValidTranslation.translation.set()


@dp.message_handler(state=ValidTranslation.translation)
async def get_text_from_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    link = data.get("post_link")
    text = message.text
    db.add_gazzetta_translation(link, text)
    await message.answer("Сохранил перевод в базе данных:")
    await message.answer(link)
    await message.answer(text)

    await state.finish()
