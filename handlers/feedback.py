"""
handlers/feedback.py — Ұсыныстар мен пікірлер жүйесі
Оқушылар мен мұғалімдер пікір қалдыра алады
"""
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)

# Админ ID (env-дан оқылады, болмаса None)
ADMIN_ID = os.getenv("ADMIN_TELEGRAM_ID")

# Пікір категориялары
FEEDBACK_CATEGORIES = {
    "fb_suggest":  ("💡", "Ұсыныс",        "Ботты жақсартуға ұсыныс"),
    "fb_error":    ("🐛", "Қате табу",      "Мазмұндағы қате туралы хабарлау"),
    "fb_thanks":   ("🙏", "Алғыс",          "Жақсы жаққа алғыс білдіру"),
    "fb_question": ("❓", "Сұрақ",          "Авторларға сұрақ қою"),
}


# ─── Негізгі пікір мәзірі ────────────────────────────────────────────────────

def feedback_menu_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = []
    for cb_key, (emoji, title, desc) in FEEDBACK_CATEGORIES.items():
        keyboard.append([InlineKeyboardButton(
            f"{emoji} {title}",
            callback_data=cb_key
        )])
    keyboard.append([InlineKeyboardButton("🏠 Бас мәзір", callback_data="menu_main")])

    query.edit_message_text(
        "📬 <b>ҰСЫНЫСТАР МЕН ПІКІРЛЕР</b>\n\n"
        "Сіздің пікіріңіз ботты жақсартуға көмектеседі!\n\n"
        "🎓 <b>Мұғалімдер, оқушылар — барлығының пікірі маңызды!</b>\n\n"
        "Санатты таңдаңыз 👇",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── Санат таңдалғанда — мәтін сұрату ───────────────────────────────────────

def feedback_category_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data  # fb_suggest / fb_error / fb_thanks / fb_question

    emoji, title, desc = FEEDBACK_CATEGORIES.get(data, ("💬", "Пікір", ""))

    # Санатты context-ке сақта
    context.user_data["feedback_category"] = data
    context.user_data["feedback_waiting"] = True

    prompts = {
        "fb_suggest":  "💡 <b>Ұсынысыңызды жазыңыз:</b>\n\nМысалы: тақырып қосу, жаңа ойын, дизайн өзгерту...",
        "fb_error":    "🐛 <b>Табылған қатені сипаттаңыз:</b>\n\nҚандай мазмұнда, қай авторда немесе сұрақта?",
        "fb_thanks":   "🙏 <b>Алғысыңызды жазыңыз:</b>\n\nНе ұнады? Не пайдалы болды?",
        "fb_question": "❓ <b>Сұрағыңызды жазыңыз:</b>\n\nАвтор, шығарма немесе ботқа байланысты кез келген сұрақ.",
    }
    prompt = prompts.get(data, "💬 Пікіріңізді жазыңыз:")

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("❌ Бас тарту", callback_data="fb_cancel")
    ]])

    query.edit_message_text(
        f"{emoji} <b>{title.upper()}</b>\n\n"
        f"{prompt}\n\n"
        f"<i>Хабарламаңызды төменге жіберіңіз 👇</i>",
        parse_mode="HTML",
        reply_markup=keyboard
    )


# ─── Мәтін алынғанда — сақтау ──────────────────────────────────────────────

def handle_feedback_text(update: Update, context: CallbackContext) -> bool:
    """
    Пайдаланушы мәтін жібергенде шақырылады.
    Пікір режимінде болса — сақтайды және True қайтарады.
    """
    if not context.user_data.get("feedback_waiting"):
        return False

    user = update.effective_user
    text = update.message.text.strip()
    category_key = context.user_data.get("feedback_category", "fb_suggest")
    emoji, title, _ = FEEDBACK_CATEGORIES.get(category_key, ("💬", "Пікір", ""))

    # DB-ге сақта
    try:
        from database import save_feedback
        save_feedback(
            user_id=user.id,
            username=user.username or "",
            full_name=user.full_name or "",
            category=category_key,
            text=text
        )
    except Exception as e:
        logger.error(f"Feedback DB error: {e}")

    # Пікір режимін өшір
    context.user_data["feedback_waiting"] = False
    context.user_data.pop("feedback_category", None)

    # Пайдаланушыға растау
    from utils.keyboards import back_to_main
    update.message.reply_text(
        f"{emoji} <b>Рақмет! Пікіріңіз қабылданды.</b>\n\n"
        f"📌 Санат: <b>{title}</b>\n"
        f"📝 Пікір: <i>{text[:200]}{'...' if len(text) > 200 else ''}</i>\n\n"
        f"Сіздің пікіріңіз ботты жақсартуға үлкен үлес қосады! 🙏",
        parse_mode="HTML",
        reply_markup=back_to_main()
    )

    # Админге хабарлама жібер
    _notify_admin(context, user, category_key, title, emoji, text)
    return True


def _notify_admin(context, user, category_key, title, emoji, text):
    """Админ ID болса — пікірді жіберу"""
    if not ADMIN_ID:
        return
    try:
        admin_msg = (
            f"📬 <b>ЖАҢА ПІКІР</b>\n\n"
            f"{emoji} <b>{title}</b>\n"
            f"👤 Пайдаланушы: {user.full_name} (@{user.username or 'жоқ'})\n"
            f"🆔 ID: <code>{user.id}</code>\n\n"
            f"💬 <b>Мазмұны:</b>\n{text}"
        )
        context.bot.send_message(
            chat_id=int(ADMIN_ID),
            text=admin_msg,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.warning(f"Admin notify error: {e}")


# ─── Бас тарту ───────────────────────────────────────────────────────────────

def feedback_cancel_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data["feedback_waiting"] = False
    context.user_data.pop("feedback_category", None)

    from utils.keyboards import back_to_main
    query.edit_message_text(
        "❌ <b>Пікір жіберу тоқтатылды.</b>\n\nБас мәзірге оралдыңыз.",
        parse_mode="HTML",
        reply_markup=back_to_main()
    )


# ─── Барлық пікірлерді көру (Админ үшін) ────────────────────────────────────

def admin_feedbacks_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = update.effective_user

    if ADMIN_ID and str(user.id) != str(ADMIN_ID):
        query.edit_message_text("❌ Рұқсат жоқ.")
        return

    try:
        from database import get_all_feedbacks
        feedbacks = get_all_feedbacks(limit=20)
    except Exception:
        feedbacks = []

    if not feedbacks:
        from utils.keyboards import back_to_main
        query.edit_message_text("📭 Әлі пікір жоқ.", reply_markup=back_to_main())
        return

    text = "📬 <b>СОҢҒЫ 20 ПІКІР</b>\n\n"
    for fb in feedbacks:
        emoji, title, _ = FEEDBACK_CATEGORIES.get(fb.get("category", ""), ("💬", "Пікір", ""))
        text += (
            f"{emoji} <b>{title}</b> — {fb.get('full_name', '')} "
            f"(@{fb.get('username', 'жоқ')})\n"
            f"<i>{fb.get('text', '')[:100]}...</i>\n"
            f"🕐 {fb.get('created_at', '')[:16]}\n\n"
        )

    from utils.keyboards import back_to_main
    query.edit_message_text(text[:4000], parse_mode="HTML", reply_markup=back_to_main())
