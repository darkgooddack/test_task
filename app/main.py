import logging

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.schemas import ProductRequest, ProductResponse
from app.crud import get_product_data
from app.db import get_db
from app.crud import create_product

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/api/v1/products", response_model=ProductResponse)
async def create_product_endpoint(request: ProductRequest, db: AsyncSession = Depends(get_db)):
    try:
        logging.info(f"🔄 Получение данных для товара с артикулом: {request.artikul}")
        product_data = await get_product_data(request.artikul)

        logging.info(f"📡 Данные о товаре получены: {product_data}")

        product_data['artikul'] = request.artikul

        product = await create_product(
            db=db,
            artikul=request.artikul,
            name=product_data["name"],
            price=product_data["price"],
            rating=product_data["rating"],
            stock_count=product_data["stock_count"]
        )

        logging.info(f"✅ Товар успешно добавлен в базу данных: {product}")

        return ProductResponse(**product_data)

    except Exception as e:
        logging.error(f"❌ Ошибка при обработке товара с артикулом {request.artikul}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))