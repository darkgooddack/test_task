import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from app.schemas import ProductRequest, ProductResponse
from app.crud import get_product_data
from app.db import get_db
from app.crud import create_product

logging.basicConfig(level=logging.INFO)

app = FastAPI()

scheduler = AsyncIOScheduler()

scheduler.start()

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


async def collect_product_data(artikul: str):
    """
    Сбор данных о товаре по артикулу и сохранение в базу данных.
    """
    # Получаем сессию базы данных
    async with get_db() as db:
        logging.info(f"🔄 Сбор данных для артикула: {artikul}")
        try:
            product_data = await get_product_data(artikul)

            logging.info(f"📡 Данные для артикула {artikul} получены: {product_data}")

            await create_product(
                db=db,
                artikul=artikul,
                name=product_data["name"],
                price=product_data["price"],
                rating=product_data["rating"],
                stock_count=product_data["stock_count"]
            )

            logging.info(f"✅ Данные для артикула {artikul} успешно добавлены в базу данных.")
        except Exception as exc:
            logging.error(f"❌ Ошибка при сборе или добавлении данных для артикула {artikul}: {exc}")
            raise exc
        finally:
            await db.close


@app.get("/api/v1/subscribe/{artikul}")
async def subscribe_product(artikul: str):
    existing_jobs = scheduler.get_jobs()
    if not any(job.id == artikul for job in existing_jobs):
        scheduler.add_job(
            collect_product_data,
            IntervalTrigger(minutes=1),
            args=[artikul],  # Передаем только артикул
            id=artikul,
            replace_existing=True,
            max_instances=1
        )
        logging.info(f"✅ Подписка на обновления для артикула {artikul} установлена.")
        return {"message": f"Subscribed to product {artikul} updates every 1 minute"}
    else:
        logging.info(f"⚠️ Подписка на артикула {artikul} уже существует.")
        return {"message": f"Already subscribed to product {artikul}"}


@app.on_event("startup")
async def startup_event():
    if not scheduler.running:
        scheduler.start()
        logging.info("📅 Планировщик задач запущен.")