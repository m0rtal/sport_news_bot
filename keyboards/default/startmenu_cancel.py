from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from .startmenu import startmenu

startmenu_cancel = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Получить обновления новостей")
        ],
        [
            KeyboardButton("Предложить свой перевод")
        ],
        [
            KeyboardButton("Отмена")
        ]
    ],
    resize_keyboard=True
)
