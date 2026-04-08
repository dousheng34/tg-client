#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kazakh Literature Bot v4.0
Telegram bot for teaching Kazakh literature (grades 1-11)
"""

import logging
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN') or os.getenv('TELEGRAM_BOT_TOKEN', '8167312154:AAFNFQqJ7_dwbbqFjlO4tTbpGSkD9lQP4rM')

# Database with Kazakh literature content (grades 1-11)
LITERATURE_DB = {
    "grades": {
        "1-4": {
            "name": "1-4 сыныптар (Бастауыш мектеп)",
            "authors": ["Халық шығармашылығы", "Ыбырай Алтынсарин"],
            "works": ["Балапан", "Еңбек етсең емерсің", "Атамекен", "Кел, балалар, оқылық"]
        },
        "5-9": {
            "name": "5-9 сыныптар (Орта мектеп)",
            "authors": ["Абай Құнанбаев", "Сәкен Сейфуллин", "Мағжан Жұмабаев", "Мұхтар Әуезов"],
            "works": ["Қара сөздер", "Тар жол, тайғақ кешу", "Батыр Баян", "Көксерек"]
        },
        "10-11": {
            "name": "10-11 сыныптар (Жоғары мектеп)",
            "authors": ["Чингиз Айтматов", "Дулат Исабеков", "Абдіжәміл Нұрпейісов"],
            "works": ["Ғасырдан да ұзақ күн", "Гауһартас", "Қан мен тер"]
        }
    },
    "authors": {
        "Абай Құнанбаев": {
            "years": "1845–1904",
            "bio": "Қазақ халқының ұлы ақыны, философы және аудармашысы",
            "works": ["Жаз", "Қыс", "Қара сөздер"]
        },
        "Мұхтар Әуезов": {
            "years": "1897–1961",
            "bio": "Қазақ ағартушысы, жазушысы және ғалымы",
            "works": ["Абай жолы", "Тоқтар", "Көксерек"]
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    user = update.effective_user
    logger.info(f"✅ Бот инициализирленді ID: {user.id}")
    
    keyboard = [
        [InlineKeyboardButton("1-4 сыныптар", callback_data="grade_1-4")],
        [InlineKeyboardButton("5-9 сыныптар", callback_data="grade_5-9")],
        [InlineKeyboardButton("10-11 сыныптар", callback_data="grade_10-11")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Сәлем, {user.first_name}! 👋\n\n"
        "Қазақ әдебиетін оқуға қош келдіңіз! 📚\n\n"
        "Өз сыныбыңды таңда:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("grade_"):
        grade = query.data.replace("grade_", "")
        grade_info = LITERATURE_DB["grades"].get(grade)
        
        if grade_info:
            text = f"📖 {grade_info['name']}\n\n"
            text += "Авторлар:\n"
            for author in grade_info['authors']:
                text += f"• {author}\n"
            text += "\nЕсептіліктер:\n"
            for work in grade_info['works']:
                text += f"• {work}\n"
            
            await query.edit_message_text(text=text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = """
    🤖 Қазақ әдебиеті бот
    
    Команды:
    /start - Бастау
    /help - Көмек
    /about - Туралы
    """
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """About command handler"""
    about_text = """
    📚 Қазақ әдебиеті бот v4.0
    
    Бұл бот қазақ әдебиетін оқуға көмектеседі.
    Барлық сыныптар үшін материалдар бар.
    """
    await update.message.reply_text(about_text)

async def main() -> None:
    """Start the bot"""
    logger.info(f"🚀 Бот басталуда... TOKEN: {BOT_TOKEN[:20]}...")
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start the bot
    logger.info("✅ Бот қосылды!")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
