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

# Koyeb нақты домені — fallback
KOYEB_BASE  = 'https://controversial-rosaleen-t44t-00f78407.koyeb.app'

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
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
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
    # Пікір жазу режимі алдымен тексер
    from handlers.feedback import handle_feedback_text
    if handle_feedback_text(update, context):
        return
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


# ── Webapp URL helper ────────────────────────────────────────────────────────────
def _get_webapp_url():
    """Mini App URL-ін дұрыс анықтайды"""
    if WEBAPP_URL:
        return WEBAPP_URL
    if WEBHOOK_URL:
        url = WEBHOOK_URL.rstrip('/')
        if '/webhook/' in url:
            url = url.split('/webhook/')[0]
        return url + '/app'
    # Хардкодталған Koyeb домені — әрқашан жұмыс істейді
    return KOYEB_BASE + '/app'


# ── /app команда — Mini App сілтемесі ───────────────────────────────────────────
def app_command(update: Update, context: CallbackContext):
    """Mini App ойын беті — /app командасы"""
    webapp_url = _get_webapp_url()

    if not webapp_url:
        update.message.reply_text(
            "⚠️ <b>Mini App тек Koyeb серверінде жұмыс істейді.</b>\n\n"
            "Жергілікті тестілеу үшін: /start → 🎮 Ойындар",
            parse_mode='HTML'
        )
        return

    from telegram import WebAppInfo
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "🎮  Ойын Кітапханасы — Ашу",
            web_app=WebAppInfo(url=webapp_url)
        )
    ]])
    update.message.reply_text(
        "🎮 <b>ҚАЗАҚ ӘДЕБИЕТІ — ОЙЫН КІТАПХАНАСЫ</b>\n\n"
        "👇 Төмендегі батырманы басыңыз.\n"
        "Ойын Telegram ішінде <b>сайт сияқты ашылады!</b>\n\n"
        "🎯 <b>6 ойын:</b> Викторина · Кім жазды? · Блиц · Цитата · Жад · Хронология\n"
        "🏆 Ұпай жүйесі · Жетістіктер · Рейтинг",
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
    elif data == "menu_terms":
        from handlers.grades import terms_callback
        terms_callback(update, context)
    elif data == "menu_app":
        _send_miniapp(update, context)
    elif data == "menu_feedback":
        from handlers.feedback import feedback_menu_callback
        feedback_menu_callback(update, context)

    # ── Пікір санаттары ───────────────────────────────────────────────
    elif data in ("fb_suggest", "fb_error", "fb_thanks", "fb_question"):
        from handlers.feedback import feedback_category_callback
        feedback_category_callback(update, context)
    elif data == "fb_cancel":
        from handlers.feedback import feedback_cancel_callback
        feedback_cancel_callback(update, context)
    elif data == "admin_feedbacks":
        from handlers.feedback import admin_feedbacks_inline_callback
        admin_feedbacks_inline_callback(update, context)

    # ── Сыныптар ─────────────────────────────────────────────────────────────
    elif data.startswith("grade_"):
        from handlers.grades import grade_select_callback
        grade_select_callback(update, context)
    elif data.startswith("topic_done_"):
        from handlers.grades import topic_done_callback
        topic_done_callback(update, context)

    # ── Тақырыптар (topics.py) ────────────────────────────────────────────────
    elif data.startswith("topics_list_"):
        # topics_list_{grade}
        grade = int(data.split("_")[-1])
        from handlers.topics import show_topics_list
        show_topics_list(update, context, grade)
    elif data.startswith("topic_read_"):
        # topic_read_{grade}_{topic_id}
        parts = data.split("_", 3)
        grade = int(parts[2]); topic_id = parts[3]
        from handlers.topics import show_topic_content
        show_topic_content(update, context, grade, topic_id)
    elif data.startswith("topic_quiz_"):
        # topic_quiz_{grade}_{topic_id}_{q_index}
        parts = data.split("_"); grade = int(parts[2])
        q_index = int(parts[-1]); topic_id = "_".join(parts[3:-1])
        from handlers.topics import show_topic_quiz
        show_topic_quiz(update, context, grade, topic_id, q_index)
    elif data.startswith("topic_answer_"):
        # topic_answer_{grade}_{topic_id}_{q_index}_{chosen}
        parts = data.split("_")
        grade = int(parts[2]); chosen = int(parts[-1]); q_index = int(parts[-2])
        topic_id = "_".join(parts[3:-2])
        from handlers.topics import check_topic_answer
        check_topic_answer(update, context, grade, topic_id, q_index, chosen)
    elif data.startswith("topic_general_quiz_"):
        # topic_general_quiz_{grade}
        grade = int(data.split("_")[-1])
        from handlers.topics import show_general_quiz
        show_general_quiz(update, context, grade)
    elif data.startswith("general_answer_"):
        # general_answer_{grade}_{q_index}_{chosen or 'show'}
        parts = data.split("_")
        grade = int(parts[2]); q_index = int(parts[3])
        if parts[4] == "show":
            from handlers.topics import show_next_general_question
            show_next_general_question(update, context, grade, q_index)
        else:
            chosen = int(parts[4])
            from handlers.topics import check_general_answer
            check_general_answer(update, context, grade, q_index, chosen)

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

    # ── Визуалды Энциклопедия ─────────────────────────────────────────────────
    elif data == "encyclopedia" or data.startswith("enc_"):
        from handlers.encyclopedia import encyclopedia_callback_handler
        encyclopedia_callback_handler(update, context)

    elif data == "main_menu":
        from handlers.menu import main_menu_callback
        main_menu_callback(update, context)

    else:
        logger.warning(f"Unknown callback: {data}")


def _send_miniapp(update: Update, context: CallbackContext):
    """Mini App батырмасын жіберу"""
    webapp_url = _get_webapp_url()
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
        "🎯 6 ойын түрі: Викторина, Кім жазды?, Цитата, Блиц, Жад, Хронология\n"
        "⏱️ Таймер, ұпай жүйесі, нәтиже экраны",
        parse_mode='HTML',
        reply_markup=keyboard
    )

# ── /feedbacks командасы — Админ үшін ──────────────────────────────────────────
def feedbacks_command(update: Update, context: CallbackContext):
    """/feedbacks — соңғы пікірлерді көру (Админ үшін)"""
    user = update.effective_user
    admin_id = os.getenv("ADMIN_TELEGRAM_ID", "")

    # Рұқсат тексеру
    if admin_id and str(user.id) != str(admin_id):
        update.message.reply_text("❌ Бұл команда тек админге қатысты.")
        return

    from database import get_all_feedbacks
    feedbacks = get_all_feedbacks(limit=20)

    CATEGORIES = {
        "fb_suggest":  ("💡", "Ұсыныс"),
        "fb_error":    ("🐛", "Қате табу"),
        "fb_thanks":   ("🙏", "Алғыс"),
        "fb_question": ("❓", "Сұрақ"),
    }

    if not feedbacks:
        update.message.reply_text("💭 Әлі пікір жоқ.\n\nОқушылар әлі ұсыныс қалдырмаған.")
        return

    # 20 пікір — бірнеше хабарламада сияды 4096 сымвол— батчалар бөлеміз
    header = f"📬 <b>ҰСЫНЫСТАР МЕН ПІКІРЛЕР ({len(feedbacks)})</b>\n"
    header += "═" * 30 + "\n\n"

    chunks = [header]
    current = header

    for i, fb in enumerate(feedbacks, 1):
        emoji, title = CATEGORIES.get(fb.get("category", ""), ("💬", "Пікір"))
        name = fb.get("full_name") or "Анықталмаған"
        uname = fb.get("username") or "жоқ"
        text = fb.get("text", "")
        dt = fb.get("created_at", "")[:16].replace("T", " ")

        entry = (
            f"{i}. {emoji} <b>{title}</b>\n"
            f"👤 {name} (@{uname})\n"
            f"📅 {dt}\n"
            f"💬 {text}\n"
            f"────────────────────────────\n\n"
        )

        if len(current) + len(entry) > 3800:
            update.message.reply_text(current, parse_mode="HTML")
            current = entry
        else:
            current += entry

    if current.strip():
        update.message.reply_text(current, parse_mode="HTML")


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
    dp.add_handler(CommandHandler("start",     start_command))
    dp.add_handler(CommandHandler("menu",      start_command))
    dp.add_handler(CommandHandler("help",      start_command))
    dp.add_handler(CommandHandler("app",       app_command))
    dp.add_handler(CommandHandler("feedbacks", feedbacks_command))
    dp.add_handler(CommandHandler("admin",     feedbacks_command))

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
