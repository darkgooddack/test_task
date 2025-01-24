import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from fastapi import Depends

from app.db import get_db
from app import crud
from sqlalchemy.ext.asyncio import AsyncSession

API_TOKEN = 'YOUR_BOT_API_TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопка для получения данных по товару
async def get_product_button():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Получить данные по товару', callback_data='get_product')
    keyboard.add(button)
    return keyboard

@dp.message(F.text in ['/start', '/help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Нажми на кнопку ниже, чтобы получить данные по товару.", reply_markup=await get_product_button())

# Обработчик нажатия на кнопку
@dp.callback_query(F.data == 'get_product')
async def ask_for_artikul(callback_query: types.CallbackQuery):
    # Спрашиваем артикул
    await bot.send_message(callback_query.from_user.id, "Введите артикул товара:")

# Обработчик текста с артикулом
@dp.message(F.text.isdigit())  # Убедимся, что введен артикул
async def fetch_product_data(message: types.Message, db: AsyncSession = Depends(get_db)):
    artikul = message.text  # Получаем артикул из текста сообщения

    # Получаем данные товара из базы данных
    product = await crud.get_product_by_artikul(db, artikul)

    if product:
        # Отправляем данные о товаре
        await message.reply(f"Товар: {product.name}\n"
                             f"Артикул: {product.artikul}\n"
                             f"Цена: {product.price} рублей\n"
                             f"Рейтинг: {product.rating}\n"
                             f"Количество на складе: {product.stock_count}", parse_mode="HTML")
    else:
        await message.reply(f"Товар с артикулом {artikul} не найден в базе данных.")

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling())
