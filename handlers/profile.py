"""handlers/profile.py — Пайдаланушы профилі мен рейтинг"""
from telegram import Update
from telegram.ext import CallbackContext
from database import (get_or_create_user, get_user_stats, get_top_users,
                      set_user_grade, LEVEL_NAMES, give_achievement)
from utils.keyboards import profile_keyboard, set_grade_keyboard, back_to_main


def profile_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = update.effective_user
    db = get_or_create_user(user.id, user.username, user.full_name)
    stats = get_user_stats(user.id)
    level = db.get('level', 1)
    emoji, level_name = LEVEL_NAMES.get(level, ("⭐", "Оқушы"))
    grade = db.get('grade', 0)
    grade_txt = f"{grade}-сынып" if grade else "Белгіленбеген"
    streak = db.get('streak', 0)
    points = db.get('points', 0)
    topics = stats.get('topics_completed', 0)
    authors = stats.get('authors_viewed', 0)
    total_games = db.get('total_games', 0)
    correct = db.get('correct_answers', 0)
    badges = stats.get('achievements', [])

    # Ойын статистикасы
    game_stats = stats.get('game_stats', [])
    games_text = ""
    for gs in game_stats:
        type_names = {
            'quiz': '🎯 Викторина', 'whowrote': '✍️ Кім жазды?',
            'findwork': '📚 Шығарманы тап', 'quote': '💬 Цитата',
            'blitz': '⚡ Блиц', 'character': '👥 Кейіпкерлер'
        }
        name = type_names.get(gs['game_type'], gs['game_type'])
        games_text += f"  {name}: {gs['cnt']} рет\n"

    text = (
        f"📊 <b>МЕН ТУРАЛЫ</b>\n"
        f"{'─'*32}\n"
        f"👤 <b>{user.full_name or user.first_name}</b>\n"
        f"{emoji} Деңгей: <b>{level} — {level_name}</b>\n"
        f"⭐ Ұпайлар: <b>{points}</b>\n"
        f"{'─'*32}\n"
        f"📚 Сыныбым: <b>{grade_txt}</b>\n"
        f"🔥 Стрик: <b>{streak} күн</b>\n"
        f"✅ Тақырыптар: <b>{topics}</b>\n"
        f"👤 Оқыған авторлар: <b>{authors}</b>\n"
        f"{'─'*32}\n"
        f"🎮 Ойындар: <b>{total_games}</b>\n"
        f"💡 Дұрыс жауаптар: <b>{correct}</b>\n"
    )
    if games_text:
        text += f"\n<b>Ойын бойынша:</b>\n{games_text}"
    if badges:
        from utils.keyboards import ACHIEVEMENTS
        badge_text = " ".join(ACHIEVEMENTS.get(b, ("🏅","",""))[0] for b in badges)
        text += f"\n🏅 Жетістіктер: {badge_text}"

    query.edit_message_text(text, parse_mode='HTML', reply_markup=profile_keyboard())


def profile_achievements_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = update.effective_user
    stats = get_user_stats(user.id)
    badges = stats.get('achievements', [])
    from utils.keyboards import ACHIEVEMENTS

    if not badges:
        text = (
            "🏅 <b>ЖЕТІСТІКТЕР</b>\n\n"
            "Әлде жетістік жоқ. Ойын ойна, тақырып оқы!\n\n"
            "<b>Алуға болатын жетістіктер:</b>\n"
        )
    else:
        earned_text = "\n".join(
            f"{ACHIEVEMENTS[b][0]} <b>{ACHIEVEMENTS[b][1]}</b> — {ACHIEVEMENTS[b][2]}"
            for b in badges if b in ACHIEVEMENTS
        )
        text = f"🏅 <b>ЖЕТІСТІКТЕРІҢ</b>\n\n{earned_text}\n\n"

    # Барлық жетістіктер
    all_text = "\n".join(
        f"{'✅' if k in badges else '🔒'} {v[0]} {v[1]}"
        for k, v in ACHIEVEMENTS.items()
    )
    text += f"<b>Барлық жетістіктер:</b>\n{all_text}"
    query.edit_message_text(text, parse_mode='HTML', reply_markup=profile_keyboard())


def profile_stats_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = update.effective_user
    stats = get_user_stats(user.id)
    db = get_or_create_user(user.id)
    total = db.get('total_games', 0)
    correct = db.get('correct_answers', 0)
    accuracy = int(correct / (total * 10) * 100) if total > 0 else 0

    text = (
        f"📈 <b>ТОЛЫҚ СТАТИСТИКА</b>\n\n"
        f"🎮 Барлық ойын: <b>{total}</b>\n"
        f"💡 Дұрыс жауаптар: <b>{correct}</b>\n"
        f"🎯 Дәлдік: <b>{min(accuracy, 100)}%</b>\n"
        f"📚 Оқыған тақырыптар: <b>{stats.get('topics_completed', 0)}</b>\n"
        f"👤 Оқыған авторлар: <b>{stats.get('authors_viewed', 0)}</b>\n"
        f"⭐ Жалпы ұпай: <b>{db.get('points', 0)}</b>\n"
        f"🔥 Стрик: <b>{db.get('streak', 0)} күн</b>\n"
    )
    query.edit_message_text(text, parse_mode='HTML', reply_markup=profile_keyboard())


def profile_set_grade_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "📚 <b>СЫНЫБЫҢДЫ ТАҢДАҢЫЗ</b>\n\n"
        "Сыныпты таңдасаңыз, ойындар мен материалдар сол сынып бойынша болады:",
        parse_mode='HTML',
        reply_markup=set_grade_keyboard()
    )


def set_grade_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    grade = int(query.data.split('_')[-1])
    set_user_grade(update.effective_user.id, grade)
    emojis = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}
    query.edit_message_text(
        f"✅ <b>{emojis.get(grade,'📚')}{grade}-сынып</b> таңдалды!\n\n"
        f"Енді ойындар {grade}-сынып материалдары бойынша болады.",
        parse_mode='HTML',
        reply_markup=back_to_main()
    )


def rating_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    top = get_top_users(10)
    if not top:
        query.edit_message_text("Рейтинг бос.", reply_markup=back_to_main())
        return

    medals = {0: "🥇", 1: "🥈", 2: "🥉"}
    lines = []
    for i, u in enumerate(top):
        medal = medals.get(i, f"{i+1}.")
        name = u.get('full_name') or u.get('username') or "Белгісіз"
        points = u.get('points', 0)
        level = u.get('level', 1)
        level_emoji = LEVEL_NAMES.get(level, ("⭐",""))[0]
        lines.append(f"{medal} {level_emoji} <b>{name}</b> — {points} ұпай")

    user_id = update.effective_user.id
    my_rank = next((i+1 for i, u in enumerate(top) if u['user_id'] == user_id), None)
    my_rank_txt = f"\n\n📍 Сенің орның: <b>{my_rank}</b>" if my_rank else ""

    query.edit_message_text(
        f"🏆 <b>ЕҢ ҮЗДІК ОҚУШЫЛАР</b>\n\n" + "\n".join(lines) + my_rank_txt,
        parse_mode='HTML',
        reply_markup=back_to_main()
    )
