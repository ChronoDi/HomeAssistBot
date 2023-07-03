from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_reply_keyboard(names: list[str], width: int = 2, is_one_time: bool = True) -> ReplyKeyboardMarkup:
    buttons: list[KeyboardButton] = []
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    for name in names:
        buttons.append(KeyboardButton(text=name))

    builder.row(*buttons, width=width)

    return builder.as_markup(on_time_keyboard=is_one_time, resize_keyboard=True)


def get_inline_keyboards(width: int, callback_names: dict[str: str]) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if callback_names:
        for button, text in callback_names.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()

