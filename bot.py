from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7564859488:AAFBjD2PdLDbaA1L76_TVVtIWU3165vW-gs"
ADMIN_ID = 7733433677

products = {
    "Одноразки": [
        {
            "name": "ELF BAR 1500",
            "desc": "Нікотин: 5%\nАкумулятор: 850 мАч\nСмаки:\n- Полуничний енергетик\n- Кисле яблуко\n- Виноградний енергетик\n- Ківі гуава маракуйя\n- Полуниця банан",
            "price": "350 грн",
            "photo": "https://i.ibb.co/dLZXpsP/elfbar.jpg"
        },
    ],
    "Готові сольові рідини": [
        {
            "name": "ELFLIQ NIC SALTS 30мл.",
            "desc": "Смаки:\n- Полуничне морозиво\n- Кола\n- Жасмин малина\n- Ананас лід\n- Подвійне яблуко",
            "price": "329 грн",
            "photo": "https://i.ibb.co/BgpvBTz/elfliq.jpg"
        }
    ],
    "Картриджі": [
        {
            "name": "VAPORESSO XROS",
            "desc": "Обʼєм: 2 мл\nОпір: 0.6 / 0.8 Ом\nСумісність: XROS MINI, 3, 3 MINI, 3 NANO, CUBE, 4 MINI, 4",
            "price": "129 грн",
            "photo": "https://i.ibb.co/8chRSb6/xros.jpg"
        }
    ],
    "Перезаряджаємі одноразки": [
        {
            "name": "ELF BAR CR 5000",
            "desc": "Смаки:\n- Лимонад Blue Razz\n- Журавлина виноградна\n- Кавун\n- Полуничне морозиво\n- Ківі Маракуйя Гуава",
            "price": "579 грн",
            "photo": "https://i.ibb.co/yfS8X1N/cr5000.jpg"
        }
    ],
    "POD-Системи": [
        {
            "name": "Lost Vape URSA NANO S",
            "desc": "Кольори: Mint Green, Violet Purple, Stone Grey\nКомплектація:\n- URSA NANO S\n- Картридж URSA 0.8 (2,5 ml)\n- Кабель Type-C\n- Інструкція",
            "price": "999 грн",
            "photo": "https://i.ibb.co/gM95n3n/ursa.jpg"
        }
    ]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cat, callback_data=cat)] for cat in products]
    await update.message.reply_text("Оберіть категорію товарів:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    items = products.get(category, [])
    for item in items:
        text = f"**{item['name']}**\n{item['desc']}\nЦіна: {item['price']}"
        buttons = [[InlineKeyboardButton("Замовити", callback_data=f"order_{item['name']}|{category}")]]
        await query.message.reply_photo(photo=item['photo'], caption=text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode='Markdown')

async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product_info = query.data.split("order_")[1]
    product_name, category = product_info.split("|")
    user = query.from_user
    msg = f"Нове замовлення:\nТовар: {product_name}\nКатегорія: {category}\nВід користувача: @{user.username or user.first_name} (ID: {user.id})"
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    await query.message.reply_text("Дякуємо за замовлення! Ми зв'яжемося з вами.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_products, pattern="^(?!order_).*"))
    app.add_handler(CallbackQueryHandler(handle_order, pattern="^order_"))
    app.run_polling()
