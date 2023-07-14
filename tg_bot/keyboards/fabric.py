from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_reply_keyboard(names: list[str], width: int = 2, is_one_time: bool = True) -> ReplyKeyboardMarkup:
    buttons: list[KeyboardButton] = []
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    for name in names:
        buttons.append(KeyboardButton(text=name))

    builder.row(*buttons, width=width)

    return builder.as_markup(on_time_keyboard=is_one_time, resize_keyboard=True)


def get_inline_keyboards(width: int,
                         callback_names: dict[str: str] | None = None,
                         special_symbol: str = None,
                         last_buttons: dict[str: str] | None = None) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if callback_names:
        for button, text in callback_names.items():
            buttons.append(InlineKeyboardButton(
                text=special_symbol + text if special_symbol else text,
                callback_data=button))

        kb_builder.row(*buttons, width=width)

    if last_buttons:
        last_buttons_list: list[InlineKeyboardButton] = []

        for button, text in last_buttons.items():
            last_buttons_list.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

        kb_builder.row(*last_buttons_list, width=len(last_buttons))

    return kb_builder.as_markup()

