from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

day_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Понедельник", callback_data="0")],
        [InlineKeyboardButton(text="Вторник", callback_data="1")],
        [InlineKeyboardButton(text="Среда", callback_data="2")],
        [InlineKeyboardButton(text="Четверг", callback_data="3")],
        [InlineKeyboardButton(text="Пятница", callback_data="4")],
        [InlineKeyboardButton(text="Суббота", callback_data="5")],
        [InlineKeyboardButton(text="Воскресенье", callback_data="6")]
    ]
)