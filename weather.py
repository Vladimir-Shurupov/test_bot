import logging
import requests
import json  # для дебага и логирования ответа

# Получаем логгер для текущего модуля
logger = logging.getLogger(__name__)

# Импортируем API ключ из config.py
from config import OWM_API_KEY

async def get_weather_from_location(latitude: float, longitude: float) -> str:
    """
    Получает данные о погоде по координатам и возвращает текстовое описание.
    """
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": OWM_API_KEY,
            "units": "metric",
            "lang": "ru"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверяем, что запрос успешен (код 200)
        data = response.json()

        logger.debug(f"OpenWeatherMap API Response: {json.dumps(data, indent=4, ensure_ascii=False)}")  # Добавляем логирование

        if data["cod"] != 200:
            logger.error(f"OpenWeatherMap API Error: {data['message']}")
            return f"Ошибка от OpenWeatherMap: {data['message']}"

        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (
            f"Погода:\n"
            f"Описание: {description}\n"
            f"Температура: {temp:.1f} °C\n"  # Форматирование температуры
            f"Влажность: {humidity} %\n"
            f"Скорость ветра: {wind_speed} м/с"
        )

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e}")
        return "Произошла ошибка HTTP при получении погоды."
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к OpenWeatherMap: {e}")
        return "Не удалось получить данные о погоде. Проверьте подключение к интернету."
    except KeyError as e:  # Обработка отсутствия ключей в ответе
        logger.error(f"KeyError: {e} - Неверный формат ответа от OpenWeatherMap")
        return "Не удалось обработать ответ от сервиса погоды. Возможно, сервис временно недоступен."
    except Exception as e:
        logger.exception(f"Ошибка при обработке данных о погоде: {e}")
        return "Произошла ошибка при получении погоды."