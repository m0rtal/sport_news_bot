from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

startmenu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Получить обновления новостей")
        ],
        [
            KeyboardButton("Предложить свой перевод")
        ]
    ],
    resize_keyboard=True
)