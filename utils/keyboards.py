"""
utils/keyboards.py — барлық клавиатуралар
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# ─── ГЛАВНОЕ МЕНЮ ──────────────────────────────────────────────────────────────

MAIN_MENU_TEXT = (
    "📚 <b>ҚАЗАҚ ӘДЕБИЕТІ — БІЛІМ КІТАПХАНАСЫ</b>\n\n"
    "Сәлем, ардақты оқушы! 👋\n"
    "Мен — қазақ әдебиетін оқуға арналған ақылды серігің.\n"
    "1-11 сынып материалдары, ойындар, авторлар — бәрі осында!\n\n"
    "👇 <b>Бөлімді таңдаңыз:</b>"
)

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📖 Сабақтар (1–11 сынып)", callback_data="menu_grades")],
        [InlineKeyboardButton("📚 Визуалды Энциклопедия", callback_data="encyclopedia")],
        [InlineKeyboardButton("👤 Авторлар", callback_data="menu_authors")],
        [InlineKeyboardButton("📊 Менің прогресім", callback_data="menu_profile"),
         InlineKeyboardButton("🏆 Рейтинг", callback_data="menu_rating")],
        [InlineKeyboardButton("📅 Күнделікті дерек", callback_data="menu_daily"),
         InlineKeyboardButton("ℹ️ Анықтама", callback_data="menu_help")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ─── Сыныптар меню ─────────────────────────────────────────────────────────────
def grades_keyboard():
    buttons = []
    row = []
    emojis = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}
    for g in range(1, 12):
        row.append(InlineKeyboardButton(f"{emojis[g]}{g}-сынып", callback_data=f"grade_{g}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 Артқа", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)

def grade_topics_keyboard(grade: int, topics: list):
    buttons = []
    for t in topics:
        buttons.append([InlineKeyboardButton(t['title'], callback_data=f"topic_{grade}_{t['key']}")])
    buttons.append([InlineKeyboardButton("🔙 Сыныптарға", callback_data="menu_grades")])
    return InlineKeyboardMarkup(buttons)

def topic_done_keyboard(grade: int):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Аяқтадым (+10 ұпай)", callback_data=f"topic_done_{grade}")],
        [InlineKeyboardButton("🔙 Сыныпқа оралу", callback_data=f"grade_{grade}")],
    ])

# ─── АВТОРЛАР МЕНЮ ─────────────────────────────────────────────────────────────
def authors_keyboard(authors_list: list):
    """authors_list = [(key, name, emoji), ...]"""
    buttons = []
    for key, name, emoji in authors_list:
        buttons.append([InlineKeyboardButton(f"{emoji} {name}", callback_data=f"author_{key}")])
    buttons.append([InlineKeyboardButton("🔙 Артқа", callback_data="menu_main")])
    return InlineKeyboardMarkup(buttons)

def author_detail_keyboard(key: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Толық өмірбаян", callback_data=f"author_full_{key}"),
         InlineKeyboardButton("📊 Инфографик", callback_data=f"author_info_{key}")],
        [InlineKeyboardButton("📚 Шығармалары", callback_data=f"author_works_{key}"),
         InlineKeyboardButton("💬 Цитаталары", callback_data=f"author_quotes_{key}")],
        [InlineKeyboardButton("🔙 Авторлар", callback_data="menu_authors")],
    ])

# ─── ОЙЫНДАР МЕНЮ ──────────────────────────────────────────────────────────────
def games_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 Викторина", callback_data="game_quiz"),
         InlineKeyboardButton("✍️ Кім жазды?", callback_data="game_whowrote")],
        [InlineKeyboardButton("📚 Шығарманы тап!", callback_data="game_findwork"),
         InlineKeyboardButton("💬 Цитата жарысы", callback_data="game_quote")],
        [InlineKeyboardButton("⚡ Блиц-тур", callback_data="game_blitz"),
         InlineKeyboardButton("👥 Кейіпкерлер", callback_data="game_character")],
        [InlineKeyboardButton("🔙 Артқа", callback_data="menu_main")],
    ])

def grade_select_for_game_keyboard(game_type: str):
    emojis = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}
    buttons = []
    row = []
    for g in range(1, 12):
        row.append(InlineKeyboardButton(f"{emojis[g]}{g}", callback_data=f"game_{game_type}_grade_{g}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🎲 Барлық класс", callback_data=f"game_{game_type}_grade_0")])
    buttons.append([InlineKeyboardButton("🔙 Ойындарға", callback_data="menu_games")])
    return InlineKeyboardMarkup(buttons)

def quiz_answer_keyboard(options: list, correct: str = None, selected: str = None):
    """Жауап нұсқалары клавиатурасы"""
    letters = ["🅰️", "🅱️", "🅲️", "🅳️"]
    buttons = []
    for i, opt in enumerate(options):
        label = f"{letters[i]} {opt}"
        if selected is not None:
            if opt == correct:
                label = f"✅ {opt}"
            elif opt == selected:
                label = f"❌ {opt}"
        buttons.append([InlineKeyboardButton(label, callback_data=f"qans_{i}")])
    return InlineKeyboardMarkup(buttons)

def next_question_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ Келесі сұрақ", callback_data="quiz_next")],
        [InlineKeyboardButton("🛑 Тоқтату", callback_data="quiz_stop")],
    ])

def game_result_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Қайталау", callback_data="menu_games"),
         InlineKeyboardButton("🏠 Бас мәзір", callback_data="menu_main")],
    ])

# ─── ПРОФИЛЬ ───────────────────────────────────────────────────────────────────
def profile_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎓 Сынып таңдау", callback_data="profile_set_grade")],
        [InlineKeyboardButton("🏆 Жетістіктерім", callback_data="profile_achievements")],
        [InlineKeyboardButton("📊 Статистика", callback_data="profile_stats")],
        [InlineKeyboardButton("🔙 Артқа", callback_data="menu_main")],
    ])

def set_grade_keyboard():
    emojis = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}
    buttons = []
    row = []
    for g in range(1, 12):
        row.append(InlineKeyboardButton(f"{emojis[g]}{g}", callback_data=f"set_grade_{g}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 Артқа", callback_data="menu_profile")])
    return InlineKeyboardMarkup(buttons)

def back_to_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Бас мәзір", callback_data="menu_main")]
    ])

def back_to_authors():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Авторларға", callback_data="menu_authors")],
        [InlineKeyboardButton("🏠 Бас мәзір", callback_data="menu_main")],
    ])

ACHIEVEMENTS = {
    "first_game":     ("🎮", "Алғашқы ойын", "Бірінші рет ойын ойнадың"),
    "quiz_master":    ("🎯", "Викторина шебері", "Викторинада 10/10 алдың"),
    "streak_3":       ("🔥", "3 күн қатарла", "3 күн қатарынан кірдің"),
    "streak_7":       ("🔥🔥", "Апталық стрик", "7 күн қатарынан кірдің"),
    "streak_30":      ("⚡", "Айлық стрик", "30 күн қатарынан кірдің"),
    "authors_5":      ("📚", "Білімді оқырман", "5 автор туралы оқыдың"),
    "authors_10":     ("📖", "Кітаппен дос", "10 автор туралы оқыдың"),
    "authors_all":    ("🏆", "Әдебиет Ұстасы", "Барлық авторларды оқыдың"),
    "points_100":     ("⭐", "100 ұпай", "100 ұпай жинадың"),
    "points_500":     ("🌟", "500 ұпай", "500 ұпай жинадың"),
    "points_1000":    ("💫", "1000 ұпай", "1000 ұпай жинадың"),
    "games_10":       ("🎯", "10 ойын", "10 рет ойын ойнадың"),
    "perfect_quiz":   ("💎", "Мінсіз викторина", "Барлық жауапты дұрыс бердің"),
    "topic_completer":("✅", "Тақырып мастері", "10 тақырып аяқтадың"),
    "level_5":        ("💫", "5-деңгей", "5-деңгейге жеттің"),
    "level_10":       ("👑", "10-деңгей", "10-деңгейге жеттің"),
}
