"""
bot.py — Қазақ Әдебиеті Telegram Боты — Бас файл
1-11 класс, ойындар, авторлар, прогресс жүйесі
"""
import logging
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler,
    MessageHandler, Filters, CallbackContext
)

from database import init_db, get_or_create_user

# ── Логирование ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ── Конфиг ───────────────────────────────────────────────────────────────────────
BOT_TOKEN   = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
PORT        = int(os.getenv('PORT', 8000))

if not BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN жоқ!")
    sys.exit(1)

# ── Health-check HTTP сервері ─────────────────────────────────────────────────────
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK - Kazakh Literature Bot')
    def log_message(self, format, *args):
        pass

def run_health_server(port: int):
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    logger.info(f"🌐 Health-check запущен на порту {port}")
    server.serve_forever()

# ── Хабарлама обработчиктері ─────────────────────────────────────────────────────
def unknown_command(update: Update, context: CallbackContext):
    from utils.keyboards import main_menu_keyboard, MAIN_MENU_TEXT
    update.message.reply_text(
        "Команда белгісіз. Мәзірді қараңыз:\n\n" + MAIN_MENU_TEXT,
        parse_mode='HTML',
        reply_markup=main_menu_keyboard()
    )

def text_message(update: Update, context: CallbackContext):
    from utils.keyboards import main_menu_keyboard
    update.message.reply_text(
        "📚 Мәзірді пайдаланыңыз:",
        reply_markup=main_menu_keyboard()
    )

def error_handler(update: Update, context: CallbackContext):
    error = context.error
    logger.error(f"Update {update} caused error: {error}")
    if "Conflict" in str(error):
        logger.warning("⚠️ Conflict: Бот екінші рет іске қосылды!")
        return
    if "Message is not modified" in str(error):
        return
    logger.error(msg="Exception:", exc_info=error)

# ── CALLBACK DISPATCHER ───────────────────────────────────────────────────────────
def callback_router(update: Update, context: CallbackContext):
    """Барлық inline callback сұрауларын бағыттайды"""
    query = update.callback_query
    data = query.data

    # ── Бас мәзір ────────────────────────────────────────────────────────────
    if data == "menu_main":
        from handlers.menu import main_menu_callback
        main_menu_callback(update, context)
    elif data == "menu_grades":
        from handlers.grades import grades_menu_callback
        grades_menu_callback(update, context)
    elif data == "menu_authors":
        from handlers.authors import authors_menu_callback
        authors_menu_callback(update, context)
    elif data == "menu_games":
        from handlers.quiz import games_menu_callback
        games_menu_callback(update, context)
    elif data == "menu_profile":
        from handlers.profile import profile_callback
        profile_callback(update, context)
    elif data == "menu_rating":
        from handlers.profile import rating_callback
        rating_callback(update, context)
    elif data == "menu_daily":
        from handlers.menu import daily_fact_callback
        daily_fact_callback(update, context)
    elif data == "menu_help":
        from handlers.menu import help_callback
        help_callback(update, context)

    # ── Сыныптар ─────────────────────────────────────────────────────────────
    elif data.startswith("grade_"):
        from handlers.grades import grade_select_callback
        grade_select_callback(update, context)
    elif data.startswith("topic_done_"):
        from handlers.grades import topic_done_callback
        topic_done_callback(update, context)
    elif data.startswith("topic_"):
        from handlers.grades import topic_callback
        topic_callback(update, context)

    # ── Авторлар ──────────────────────────────────────────────────────────────
    elif data.startswith("author_full_"):
        from handlers.authors import author_full_callback
        author_full_callback(update, context)
    elif data.startswith("author_info_"):
        from handlers.authors import author_infographic_callback
        author_infographic_callback(update, context)
    elif data.startswith("author_works_"):
        from handlers.authors import author_works_callback
        author_works_callback(update, context)
    elif data.startswith("author_quotes_"):
        from handlers.authors import author_quotes_callback
        author_quotes_callback(update, context)
    elif data.startswith("author_"):
        from handlers.authors import author_card_callback
        author_card_callback(update, context)

    # ── Ойындар ───────────────────────────────────────────────────────────────
    elif data == "game_quiz":
        from handlers.quiz import game_quiz_start
        game_quiz_start(update, context)
    elif data == "game_whowrote":
        from handlers.quiz import game_whowrote_start
        game_whowrote_start(update, context)
    elif data == "game_findwork":
        from handlers.quiz import game_findwork_start
        game_findwork_start(update, context)
    elif data == "game_quote":
        from handlers.quiz import game_quote_start
        game_quote_start(update, context)
    elif data == "game_blitz":
        from handlers.quiz import game_blitz_start
        game_blitz_start(update, context)
    elif data == "game_character":
        from handlers.quiz import game_character_start
        game_character_start(update, context)

    # ── Ойын сынып таңдау ─────────────────────────────────────────────────────
    elif "grade_" in data and data.startswith("game_"):
        from handlers.quiz import game_grade_selected
        game_grade_selected(update, context)

    # ── Викторина жауаптары ────────────────────────────────────────────────────
    elif data.startswith("qans_"):
        from handlers.quiz import quiz_answer_callback
        quiz_answer_callback(update, context)
    elif data == "quiz_next":
        from handlers.quiz import quiz_next_callback
        quiz_next_callback(update, context)
    elif data == "quiz_stop":
        from handlers.quiz import quiz_stop_callback
        quiz_stop_callback(update, context)

    # ── Кім жазды жауаптары ───────────────────────────────────────────────────
    elif data.startswith("wa_ans_"):
        from handlers.quiz import wa_answer_callback
        wa_answer_callback(update, context)
    elif data == "wa_next":
        from handlers.quiz import wa_next_callback
        wa_next_callback(update, context)
    elif data == "wa_stop":
        from handlers.quiz import wa_stop_callback
        wa_stop_callback(update, context)

    # ── Профиль ───────────────────────────────────────────────────────────────
    elif data == "profile_achievements":
        from handlers.profile import profile_achievements_callback
        profile_achievements_callback(update, context)
    elif data == "profile_stats":
        from handlers.profile import profile_stats_callback
        profile_stats_callback(update, context)
    elif data == "profile_set_grade":
        from handlers.profile import profile_set_grade_callback
        profile_set_grade_callback(update, context)
    elif data.startswith("set_grade_"):
        from handlers.profile import set_grade_callback
        set_grade_callback(update, context)

    else:
        query.answer("❓ Белгісіз команда")
        logger.warning(f"Unknown callback: {data}")


# ── MAIN ─────────────────────────────────────────────────────────────────────────
def main() -> None:
    logger.info("🚀 Қазақ Әдебиеті Боты іске қосылуда...")

    # Дерекқорды іске қосу
    init_db()
    logger.info("✅ Дерекқор дайын")

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Командалар
    from handlers.menu import start_command
    dp.add_handler(CommandHandler("start",  start_command))
    dp.add_handler(CommandHandler("menu",   start_command))
    dp.add_handler(CommandHandler("help",   start_command))

    # Барлық callback — бір роутер арқылы
    dp.add_handler(CallbackQueryHandler(callback_router))

    # Белгісіз хабарлар
    dp.add_handler(MessageHandler(Filters.command, unknown_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))

    # Қате өңдеуші
    dp.add_error_handler(error_handler)

    if WEBHOOK_URL:
        # ── WEBHOOK (продакшн: Koyeb / Heroku) ───────────────────────────────
        health_thread = threading.Thread(
            target=run_health_server, args=(PORT,), daemon=True
        )
        health_thread.start()

        webhook_path = f"/webhook/{BOT_TOKEN}"
        full_url = f"{WEBHOOK_URL.rstrip('/')}{webhook_path}"

        logger.info(f"✅ WEBHOOK режимі: {full_url}")
        updater.start_webhook(
            listen='0.0.0.0',
            port=PORT + 1,
            url_path=webhook_path,
            webhook_url=full_url,
            drop_pending_updates=True,
        )
    else:
        # ── POLLING (жергілікті) ──────────────────────────────────────────────
        logger.info("✅ POLLING режимі (жергілікті)")
        updater.start_polling(drop_pending_updates=True, timeout=20)

    logger.info("🎓 Бот жұмыс істеп тұр!")
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Қате: {e}")
        sys.exit(1)
