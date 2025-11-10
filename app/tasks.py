from app_celery import celery
from services.apartment_embedding import apartment_embedding
from services.rent_embedding import rent_embedding
import logging

logger = logging.getLogger(__name__)


@celery.task(name='tasks.embed_apartments', bind=True)
def embed_apartments(self):
    try:
        logger.info("Начало ембеддинга квартир")
        result = apartment_embedding() or []
        logger.info(f"Квартиры успешно обработаны")
        return {'status': 'success'}
    except Exception as e:
        logger.error(f"Ошибка эмбеддинга квартир: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)


@celery.task(name='tasks.embed_rent', bind=True)
def embed_rent(self):
    try:
        logger.info("Начало ембеддинга арендных квартир")
        result = rent_embedding() or []
        logger.info(f"Квартиры успешно арендных обработаны")
        return {'status': 'success'}
    except Exception as e:
        logger.error(f"Ошибка эмбеддинга арендных квартир: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
