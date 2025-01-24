# API для работы с продуктами Wildberries

Этот проект представляет собой API, которое собирает данные о товарах с сайта Wildberries и сохраняет их в базе данных. API позволяет получать данные о товарах по артикулу, создавать новые продукты и подписываться на периодический сбор данных о товаре.

## Доступ к документации

Swagger UI: http://127.0.0.1:8080/docs

## Функциональность

- Получение данных о продукте по артикулу.
- Создание нового продукта в базе данных.
- Подписка на периодический сбор данных по товару с указанным артикулом.

## Структура проекта

- **`main.py`** — основной файл с реализацией API на FastAPI.
- **`crud.py`** — файл с функциями для взаимодействия с базой данных.
- **`models.py`** — описание моделей базы данных.
- **`schemas.py`** — описание схем данных (используются для валидации запросов и ответов).
- **`db.py`** — файл для работы с базой данных и сессиями.
- **`config.py`** — файл для доступа к чувствительным данным.

## Установка

Для начала работы с проектом необходимо установить все зависимости. Для этого выполните следующие шаги:

1. Клонируйте репозиторий:
   ```
   https://github.com/darkgooddack/test_task.git
    ```
2. Перейдите в директорию проекта:
    ```
    cd test_task
    ```
3. Создайте виртуальное окружение:
    ```
    python -m venv .venv
    ```
4. Активируйте виртуальное окружение:
    ```
    .venv\Scripts\activate
    ```
5. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```
6. Для запуска приложения используйте команду:
    ```
    python -m uvicorn app.main:app --port 8080
    ```
7. Создайте файл .env и заполните его по аналогии с .env.example
8. Проведите миграции
    ```
    alembic revision --autogenerate -m "Описание изменений"
    ```
9. Чтобы применить последнюю миграцию, выполните команду:
    ```
    alembic upgrade head
    ```

## API
### POST /api/v1/products/{artikul}
Этот эндпоинт позволяет создать новый продукт. Для этого необходимо передать в запрос артикул товара:
Пример запроса:
```
    GET /api/v1/products/123456
```
Пример ответа:
```
    {
        "id": 1,
        "artikul": "123456",
        "name": "Товар 1",
        "price": 1000,
        "rating": 4.5,
        "stock_count": 50
    }
```
### GET /api/v1/subscribe/{artikul}
Этот эндпоинт позволяет подписаться на периодический сбор данных о товаре с указанным артикулом. Данные будут собираться каждые 30 минут.
Пример запроса:
```
    GET /api/v1/subscribe/123456
```
Пример ответа:
```
{
    "message": "Started periodic data collection for product 123456 every 30 minutes."
}
```