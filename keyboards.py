from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_keyboard(with_location: bool = False):
    """
    Создает основную клавиатуру.

    Args:
        with_location:  Если True, добавляет кнопку "Погода".
    """
    keyboard_buttons = [
        [
            KeyboardButton(text="Стоп"),
            KeyboardButton(text="Покажи лису"),
        ],
        [
            KeyboardButton(text="Подписка"), # Заменяем "Закрыть" на "Подписка"
        ]
    ]

    if with_location:
        keyboard_buttons[1].insert(0, KeyboardButton(text="Погода"))  # Добавляем "Погоду"

    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard_buttons,
        resize_keyboard=True
    )
    return keyboard


def create_subscription_keyboard():
    """
    Создает клавиатуру для выбора варианта подписки.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Оформить подписку"),
            ],
            [
                KeyboardButton(text="Продолжить бесплатно"),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard