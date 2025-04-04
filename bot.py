import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = '7564859488:AAFBjD2PdLDbaA1L76_TVVtIWU3165vW-gs'
ADMIN_ID = 7733433677  # Твій Telegram ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# --- Головне меню ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("POD-Системи", callback_data='pod'))
    keyboard.add(types.InlineKeyboardButton("Готові сольові рідини", callback_data='salt'))
    keyboard.add(types.InlineKeyboardButton("Картриджі", callback_data='cartridge'))
    keyboard.add(types.InlineKeyboardButton("Перезаряджаємі одноразки", callback_data='rechargeable'))
    keyboard.add(types.InlineKeyboardButton("Одноразки", callback_data='disposable'))
    await message.answer("Оберіть категорію товарів:", reply_markup=keyboard)

# --- Повернення в головне меню ---
@dp.callback_query_handler(lambda c: c.data == 'back_main')
async def back_main(callback_query: types.CallbackQuery):
    await send_welcome(callback_query.message)

# --- Категорії ---
@dp.callback_query_handler(lambda c: c.data == 'pod')
async def show_pod(callback_query: types.CallbackQuery):
    photo = InputFile("images/pod.jpg")
    caption = (
        "**Lost Vape URSA NANO S**\n"
        "Колір: Mint Green, Violet Purple, Stone Grey\n\n"
        "**Комплектація:**\n"
        "- POD-Система URSA NANO S\n"
        "- Картридж URSA 0.8 (2.5 мл)\n"
        "- Кабель Type-C\n"
        "- Інструкція\n"
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Замовити", callback_data='order_pod'))
    keyboard.add(types.InlineKeyboardButton("Назад", callback_data='back_main'))
    await bot.send_photo(callback_query.from_user.id, photo, caption=caption, parse_mode='Markdown', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'salt')
async def show_salt(callback_query: types.CallbackQuery):
    photo = InputFile("images/salt.jpg")
    caption = (
        "**ELFLIQ NIC SALTS 30мл.**\n"
        "Смаки: Полуничне морозиво, Кола, Жасмин-малина, Ананас-лід, Подвійне яблуко\n"
        "Ціна: *329 грн*"
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Замовити", callback_data='order_salt'))
    keyboard.add(types.InlineKeyboardButton("Назад", callback_data='back_main'))
    await bot.send_photo(callback_query.from_user.id, photo, caption=caption, parse_mode='Markdown', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'cartridge')
async def show_cartridge(callback_query: types.CallbackQuery):
    photo = InputFile("images/cartridge.jpg")
    caption = (
        "**Картриджі VAPORESSO XROS**\n"
        "Обʼєм: 2 мл | Опір: 0.6 / 0.8 Ом\n"
        "Підходить для:\n"
        "- XROS MINI, XROS 3, XROS 3 MINI, XROS 4 тощо\n"
        "Ціна: *129 грн*"
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Замовити", callback_data='order_cartridge'))
    keyboard.add(types.InlineKeyboardButton("Назад", callback_data='back_main'))
    await bot.send_photo(callback_query.from_user.id, photo, caption=caption, parse_mode='Markdown', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'rechargeable')
async def show_rechargeable(callback_query: types.CallbackQuery):
    photo = InputFile("images/rechargeable.jpg")
    caption = (
        "**ELF BAR CR5000**\n"
        "Смаки: Лимонад Blue Razz, Журавлина-виноград, Кавун, Полуничне морозиво, Ківі-Маракуйя-Гуава\n"
        "Ціна: *579 грн*"
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Замовити", callback_data='order_cr5000'))
    keyboard.add(types.InlineKeyboardButton("Назад", callback_data='back_main'))
    await bot.send_photo(callback_query.from_user.id, photo, caption=caption, parse_mode='Markdown', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'disposable')
async def show_disposable(callback_query: types.CallbackQuery):
    photo = InputFile("images/disposable.jpg")
    caption = (
        "**ELF BAR 1500**\n"
        "Смаки: Полуничний енергетик, Кисле яблуко, Виноградний енергетик, Ківі-Гуава-Маракуйя, Полуниця-Банан\n"
        "Ціна: *350 грн*"
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Замовити", callback_data='order_disposable'))
    keyboard.add(types.InlineKeyboardButton("Назад", callback_data='back_main'))
    await bot.send_photo(callback_query.from_user.id, photo, caption=caption, parse_mode='Markdown', reply_markup=keyboard)

# --- Обробка замовлень ---
@dp.callback_query_handler(lambda c: c.data.startswith('order_'))
async def handle_order(callback_query: types.CallbackQuery):
    product = callback_query.data.split('_')[1]
    await callback_query.answer("Дякуємо за замовлення! Ми з вами звʼяжемося.")
    await bot.send_message(
        ADMIN_ID,
        f"Користувач @{callback_query.from_user.username or callback_query.from_user.id} зробив замовлення: {product.upper()}"
    )

# --- Запуск ---
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)