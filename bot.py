"""
bot.py — Қазақ Әдебиеті Telegram Боты — Бас файл
1-11 класс, ойындар, авторлар, прогресс жүйесі, Mini App
"""
import logging
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
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
WEBAPP_URL  = os.getenv('WEBAPP_URL', '')   # Mini App URL (автоматты анықталады)

if not BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN жоқ!")
    sys.exit(1)

# ── Health-check + Mini App HTTP сервері ──────────────────────────────────────────
WEBAPP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webapp')

class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('OK - Kazakh Literature Bot'.encode())
        elif self.path == '/app' or self.path == '/app/':
            self._serve_file(os.path.join(WEBAPP_DIR, 'index.html'), 'text/html; charset=utf-8')
        else:
            self.send_response(404)
            self.end_headers()

    def _serve_file(self, path, content_type):
        try:
            with open(path, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def run_health_server(port: int):
    try:
        server = HTTPServer(('0.0.0.0', port), AppHandler)
        logger.info(f"🌐 Health+WebApp сервері: port {port}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"Сервер қатесі: {e}")


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


# ── /app команда — Mini App сілтемесі ───────────────────────────────────────────
def app_command(update: Update, context: CallbackContext):
    """Mini App ойын беті"""
    webapp_url = WEBAPP_URL or (
        WEBHOOK_URL.rstrip('/') + '/app' if WEBHOOK_URL else None
    )
    if not webapp_url:
        update.message.reply_text(
            "⚠️ Mini App тек деплой (Koyeb) серверінде жұмыс істейді.\n"
            "Бот арқылы ойнау үшін: /start → 🎮 Ойындар"
        )
        return

    from telegram import WebAppInfo
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="🎮 Ойынды ашу",
            web_app=WebAppInfo(url=webapp_url)
        )
    ]])
    update.message.reply_text(
        "🎮 <b>ҚАЗАҚ ӘДЕБИЕТІ — ИНТЕРАКТИВТІ ОЙЫН</b>\n\n"
        "📱 Ойынды ашу үшін төмендегі батырманы басыңыз!\n\n"
        "🎯 Визорина, Цитата, Блиц — барлығы осында!\n"
        "⏱️ Таймер + Ұпай жүйесі + Нәтиже!",
        parse_mode='HTML',
        reply_markup=keyboard
    )


# ── CALLBACK DISPATCHER ───────────────────────────────────────────────────────────
def callback_router(update: Update, context: CallbackContext):
    """Барлық inline callback сұрауларын бағыттайды"""
    query = update.callback_query
    query.answer()   # ← БІРІНШІ қатарда: жылдам жауап (<0.5с)
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
    elif data == "menu_app":
        _send_miniapp(update, context)

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
    elif data.startswith("game_") and "_grade_" in data:
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
        logger.warning(f"Unknown callback: {data}")


def _send_miniapp(update: Update, context: CallbackContext):
    """Mini App батырмасын жіберу"""
    webapp_url = WEBAPP_URL or (
        WEBHOOK_URL.rstrip('/') + '/app' if WEBHOOK_URL else None
    )
    query = update.callback_query
    if not webapp_url:
        query.edit_message_text(
            "⚠️ Mini App тек деплой серверінде жұмыс істейді.\n"
            "Бот ішіндегі ойынды қараңыз: 🎮 Ойындар"
        )
        return
    from telegram import WebAppInfo
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("🎮 Ойынды ашу (Mini App)", web_app=WebAppInfo(url=webapp_url))
    ], [
        InlineKeyboardButton("◀️ Артқа", callback_data="menu_main")
    ]])
    query.edit_message_text(
        "🎮 <b>ОЙЫН — MINI APP</b>\n\n"
        "💡 Батырманы басыңыз — ойын ашылады!\n"
        "🎯 4 ойын түрі: Викторина, Кім жазды?, Цитата, Блиц\n"
        "⏱️ Таймер, ұпай жүйесі, нәтиже экраны",
        parse_mode='HTML',
        reply_markup=keyboard
    )


# ── MAIN ─────────────────────────────────────────────────────────────────────────
def main() -> None:
    logger.info("🚀 Қазақ Әдебиеті Боты іске қосылуда...")

    # 1. Дерекқор
    init_db()
    logger.info("✅ Дерекқор дайын")

    # 2. Health+WebApp серверін БІРІНШІ қос (Koyeb TCP health check талабы)
    health_thread = threading.Thread(
        target=run_health_server, args=(PORT,), daemon=True
    )
    health_thread.start()

    # 3. Updater
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Командалар
    from handlers.menu import start_command
    dp.add_handler(CommandHandler("start",  start_command))
    dp.add_handler(CommandHandler("menu",   start_command))
    dp.add_handler(CommandHandler("help",   start_command))
    dp.add_handler(CommandHandler("app",    app_command))

    # Барлық callback
    dp.add_handler(CallbackQueryHandler(callback_router))

    # Белгісіз хабарлар
    dp.add_handler(MessageHandler(Filters.command, unknown_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))

    # Қате өңдеуші
    dp.add_error_handler(error_handler)

    if WEBHOOK_URL:
        # ── WEBHOOK режимі (Koyeb production) ───────────────────────────────
        bot_port     = PORT + 1
        webhook_path = f"/webhook/{BOT_TOKEN}"
        full_url     = f"{WEBHOOK_URL.rstrip('/')}{webhook_path}"

        logger.info(f"✅ WEBHOOK режимі: {full_url}")
        logger.info(f"   Health+WebApp: :{PORT}  |  Bot: :{bot_port}")
        updater.start_webhook(
            listen='0.0.0.0',
            port=bot_port,
            url_path=webhook_path,
            webhook_url=full_url,
            drop_pending_updates=True,
        )
    else:
        # ── POLLING режимі (жергілікті) ──────────────────────────────────────
        try:
            updater.bot.delete_webhook(drop_pending_updates=True)
            logger.info("🧹 Webhook тазартылды")
        except Exception as e:
            logger.warning(f"Webhook тазарту қатесі: {e}")

        logger.info("✅ POLLING режимі")
        updater.start_polling(drop_pending_updates=True, timeout=20, poll_interval=1.0)

    logger.info("🎓 Бот жұмыс істеп тұр!")
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Қате: {e}")
        sys.exit(1)
