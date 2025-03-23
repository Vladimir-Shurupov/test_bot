import logging
import requests
import json

# Получаем логгер для текущего модуля
logger = logging.getLogger(__name__)

async def get_random_fox_image_url() -> str:
    """
    Получает URL случайной фотографии лисы из API randomfox.ca.
    """
    try:
        response = requests.get("https://randomfox.ca/floof/")
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Response from randomfox.ca: {json.dumps(data, indent=4, ensure_ascii=False)}")
        return data["image"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к randomfox.ca: {e}")
        return None
    except Exception as e:
        logger.exception(f"Ошибка при обработке ответа от randomfox.ca: {e}")
        return None