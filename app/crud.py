from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Product
import httpx
from typing import Dict, Any

import httpx
from typing import Dict, Any
import logging

async def create_product(db: AsyncSession, name: str, artikul: str, price: float, rating: float, stock_count: int):
    new_product = Product(
        name=name,
        artikul=artikul,
        price=price,
        rating=rating,
        stock_count=stock_count
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


async def get_product_data(artikul: str) -> Dict[str, Any]:
    """
    Получает данные о товаре с Wildberries по артикулу.

    :param artikul: Артикул товара на Wildberries.
    :return: Словарь с данными о товаре (название, цена, рейтинг, количество на складах).
    """

    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"

    async with httpx.AsyncClient() as client:
        try:
            logging.info(f"🔄 Отправка запроса к API Wildberries для артикула: {artikul}")
            response = await client.get(url)
            logging.info(f"📡 Получен ответ от API с кодом: {response.status_code}")

            if response.status_code != 200:
                raise ValueError(
                    f"❌ Ошибка при получении данных для артикула {artikul}: {response.status_code}, Ответ: {response.text}")

            data = response.json()
            #logging.info(f"✅ Получены данные: {data}")
            logging.info(f"✅ Получены данные")

            products = data.get("data", {}).get("products", [])
            if not products:
                raise ValueError(f"❌ Продукт с артикулом {artikul} не найден в ответе от API")

            product_data = products[0]
            return {
                "name": product_data.get("name"),
                "price": product_data.get("priceU", 0) / 100,
                "rating": product_data.get("rating", 0),
                "stock_count": product_data.get("quantity", 0)
            }


        except httpx.RequestError as exc:
            logging.error(f"⚠️ Произошла ошибка при запросе к API Wildberries: {exc}")
            raise ValueError(f"⚠️ Произошла ошибка при запросе к API Wildberries: {exc}")


        except Exception as exc:
            logging.error(f"❗ Произошла непредвиденная ошибка: {exc}")
            raise ValueError(f"❗ Произошла непредвиденная ошибка: {exc}")