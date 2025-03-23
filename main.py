import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
import config
import keyboards
import weather
import fox

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# Получаем логгер для текущего модуля
logger = logging.getLogger(__name__)

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота, полученный от BotFather
BOT_TOKEN = config.token

# Инициализируем бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    Этот обработчик реагирует на команду /start и отправляет клавиатуру.
    """
    user_id = message.from_user.id
    user_name = message.from_user.username
    logger.info(f"User {user_id} (username: {user_name}) started the bot.")

    keyboard = keyboards.create_keyboard(with_location=True)  # Начальная клавиатура
    await message.answer(f"Привет {user_name}! Выбери кнопку:", reply_markup=keyboard)


# Обработчик нажатия кнопки "Стоп"
@dp.message(~F.location, lambda message: message.text.lower() == "стоп")
async def stop_button_handler(message: types.Message) -> None:
    """
    Обработчик нажатия кнопки "Стоп".
    """
    user_id = message.from_user.id
    logger.info(f"User {user_id} pressed the 'Стоп' button.")
    await message.answer("Бот остановлен. Для повторного запуска используйте /start",
                         reply_markup=keyboards.create_keyboard(with_location=True))


# Обработчик нажатия кнопки "Погода"
@dp.message(~F.location, lambda message: message.text.lower() == "погода")
async def weather_button_handler(message: types.Message) -> None:
    """
    Обработчик нажатия кнопки "Погода".  Запрашивает местоположение пользователя.
    """
    user_id = message.from_user.id
    logger.info(f"User {user_id} pressed the 'Погода' button.")

    # Запрашиваем местоположение
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(
                    text="Отправить местоположение", request_location=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True  # Клавиатура исчезнет после нажатия
    )
    await message.answer(
        "Пожалуйста, отправьте свое местоположение:", reply_markup=keyboard
    )


# Обработчик местоположения
@dp.message(F.location)  # Используем F.location для фильтрации по типу контента
async def location_handler(message: types.Message) -> None:
    """
    Обработчик получения местоположения от пользователя.
    """
    user_id = message.from_user.id
    latitude = message.location.latitude
    longitude = message.location.longitude
    logger.info(
        f"User {user_id} sent location: Latitude={latitude}, Longitude={longitude}"
    )

    # Получаем данные о погоде
    weather_description = await weather.get_weather_from_location(latitude, longitude) #вызываем функцию из модуля weather

    # Отправляем погоду пользователю
    await message.answer(weather_description,
                         reply_markup=keyboards.create_keyboard(with_location=True))  # Возвращаем основную клавиатуру


# Обработчик нажатия кнопки "Покажи лису"
@dp.message(~F.location, lambda message: message.text.lower() == "покажи лису")
async def fox_button_handler(message: types.Message) -> None:
    """
    Обработчик нажатия кнопки "Покажи лису".
    """
    user_id = message.from_user.id
    logger.info(f"User {user_id} pressed the 'Покажи лису' button.")

    # Получаем случайный URL фотографии лисы
    fox_photo_url = await fox.get_random_fox_image_url() #вызываем функцию из модуля fox

    if fox_photo_url:
        try:
            await bot.send_photo(chat_id=message.chat.id, photo=fox_photo_url)
        except Exception as e:
            logger.error(f"Failed to send fox picture to user {user_id}: {e}")
            await message.answer("Не удалось отправить фото лисы.")
    else:
        await message.answer("Не удалось получить фото лисы. Попробуйте позже.")


# Обработчик нажатия кнопки "Подписка"
@dp.message(~F.location, lambda message: message.text.lower() == "подписка")
async def subscription_handler(message: types.Message) -> None:
    """
    Обработчик нажатия кнопки "Подписка".
    """
    user_id = message.from_user.id
    logger.info(f"User {user_id} pressed the 'Подписка' button.")

    keyboard = keyboards.create_subscription_keyboard() # Создаем клавиатуру для подписки
    await message.answer("Выберите вариант подписки:", reply_markup=keyboard)


# Обработчик нажатия кнопки "Оформить подписку"
@dp.message(~F.location, lambda message: message.text.lower() == "оформить подписку")
async def subscribe_handler(message: types.Message) -> None:
    """
    Обработчик нажатия кнопки "Оформить подписку".
    """
    user_id = message.from_user.id
    logger.info(f"User {user_id} pressed the 'Оформить подписку' button.")
    await message.answer("Шутка! У нас тут все бесплатно, это просто учебный бот)",
                         reply_markup=keyboards.create_keyboard(with_location=True)) # Возвращаемся на главную


# Обработчик нажатия кнопки "Продолжить бесплатно"
@dp.message(~F.location, lambda message: message.text.lower() == "продолжить бесплатно")
async def continue_free_handler(message: types.Message) -> None:
    """
    Обработчик нажатия кнопки "Продолжить бесплатно".
    """
    user_id = message.from_user.id
    logger.info(f"User {user_id} pressed the 'Продолжить бесплатно' button.")
    await message.answer("Продолжайте пользоваться ботом бесплатно!",
                         reply_markup=keyboards.create_keyboard(with_location=True))  # Возвращаемся на главную



# Обработчик всех остальных сообщений (эхо)
@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Этот обработчик просто повторяет все полученные сообщения,
    если это не команда, не нажатие кнопки и не местоположение.
    """
    user_id = message.from_user.id
    try:
        # Отправляем то же сообщение, которое получили
        await message.send_copy(chat_id=message.chat.id)
        logger.info(f"Echoed message from user {user_id}: {message.text}")  # Логируем эхо сообщение
    except TypeError as e:
        # Если сообщение не может быть скопировано (например, стикер),
        # отправляем текстовое сообщение об этом.  Это хорошая практика.
        await message.answer("Не могу это повторить :(")
        logger.warning(f"Could not echo message from user {user_id} (TypeError): {e}")
    except Exception as e:  # Ловим любые другие исключения
        logger.error(f"Error echoing message from user {user_id}: {e}", exc_info=True)  # Логируем с информацией об исключении


async def main() -> None:
    """
    Запускаем бот
    """
    try:
        # Запускаем polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical("Bot polling failed!", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())