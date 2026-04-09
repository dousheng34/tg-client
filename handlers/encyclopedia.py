"""
handlers/encyclopedia.py
Визуалды энциклопедия handler — 1-11 сынып
PTB v13 (синхронды) нұсқасы
"""

import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

try:
    from content.encyclopedia import ENCYCLOPEDIA
except ImportError:
    ENCYCLOPEDIA = {}

try:
    from content.quiz_bank import QUIZ_BANK
except ImportError:
    QUIZ_BANK = {}


# ─── Деректерге оңай қолжетімділік ─────────────────────────────────────────

def _grade(g):
    return ENCYCLOPEDIA.get(g, {})

def _authors(g):
    return _grade(g).get("authors", {})

def _works(g):
    return _grade(g).get("works", {})

def _characters(g):
    return _grade(g).get("characters", {})

def _themes(g):
    return _grade(g).get("themes", [])

def _facts(g):
    return _grade(g).get("facts", [])

def _terms(g):
    return _grade(g).get("terms", {})

def _quiz(g):
    return QUIZ_BANK.get(g, [])


# ─── Бас мәзір ─────────────────────────────────────────────────────────────

def show_encyclopedia_menu(update: Update, context: CallbackContext):
    """Энциклопедия — сыныптар тізімі"""
    query = update.callback_query
    query.answer()

    emojis = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}
    grade_titles = {
        1:"1-сынып", 2:"2-сынып", 3:"3-сынып", 4:"4-сынып",
        5:"5-сынып", 6:"6-сынып", 7:"7-сынып", 8:"8-сынып",
        9:"9-сынып", 10:"10-сынып", 11:"11-сынып"
    }

    keyboard = []
    row = []
    for g in range(1, 12):
        em = emojis.get(g, "📖")
        title = _grade(g).get("title") or grade_titles.get(g, f"{g}-сынып")
        # Батырма мәтіні қысқа: "🌱 1-сынып"
        short = title.split("—")[0].strip() if "—" in title else title
        row.append(InlineKeyboardButton(f"{em} {short}", callback_data=f"enc_grade_{g}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🏠 Бас мәзір", callback_data="menu_main")])

    quiz_total = sum(len(v) for v in QUIZ_BANK.values())
    text = (
        "<b>📚 ВИЗУАЛДЫ ЭНЦИКЛОПЕДИЯ</b>\n\n"
        "🎓 1-11 сынып бойынша толық контент:\n"
        "• 👨‍🏫 Авторлар өмірбаяны\n"
        "• 📖 Шығармалар талдауы\n"
        "• 🎭 Кейіпкерлер сипаты\n"
        "• 💡 Қызықты деректер\n"
        f"• 🎯 Тест сұрақтары: <b>{quiz_total}+</b>\n"
        "• 📑 Терминдер сөздігі\n\n"
        "👇 <b>Сыныпты таңдаңыз:</b>"
    )
    query.edit_message_text(
        text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── Сынып бөлімдері ────────────────────────────────────────────────────────

def show_grade_menu(update: Update, context: CallbackContext, grade_num: int):
    """Сынып ішіндегі бөлімдер"""
    query = update.callback_query
    query.answer()

    grade = _grade(grade_num)
    emojis = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}
    em = emojis.get(grade_num, "📖")

    a_count = len(_authors(grade_num))
    w_count = len(_works(grade_num))
    c_count = len(_characters(grade_num))
    th_count = len(_themes(grade_num))
    f_count = len(_facts(grade_num))
    tr_count = len(_terms(grade_num))
    q_count = len(_quiz(grade_num))

    keyboard = [
        [InlineKeyboardButton(f"👨‍🏫 Авторлар ({a_count})", callback_data=f"enc_authors_{grade_num}")],
        [InlineKeyboardButton(f"📖 Шығармалар ({w_count})", callback_data=f"enc_works_{grade_num}")],
        [InlineKeyboardButton(f"🎭 Кейіпкерлер ({c_count})", callback_data=f"enc_chars_{grade_num}")],
        [InlineKeyboardButton(f"🌟 Тақырыптар ({th_count})", callback_data=f"enc_themes_{grade_num}")],
        [InlineKeyboardButton(f"💡 Қызықты деректер ({f_count})", callback_data=f"enc_facts_{grade_num}")],
        [InlineKeyboardButton(f"📑 Терминдер ({tr_count})", callback_data=f"enc_terms_{grade_num}")],
        [InlineKeyboardButton(f"🎯 Тест ({q_count} сұрақ)", callback_data=f"enc_quiz_{grade_num}_0")],
        [InlineKeyboardButton("◀️ Сыныптар", callback_data="encyclopedia"),
         InlineKeyboardButton("🏠 Бас мәзір", callback_data="menu_main")],
    ]

    title = grade.get("title", f"{grade_num}-сынып")
    text = (
        f"{em} <b>{title}</b>\n\n"
        f"📊 <b>Мазмұн:</b>\n"
        f"• 👨‍🏫 {a_count} автор\n"
        f"• 📖 {w_count} шығарма\n"
        f"• 🎭 {c_count} кейіпкер\n"
        f"• 🌟 {th_count} тақырып\n"
        f"• 💡 {f_count} қызықты дерек\n"
        f"• 📑 {tr_count} термин\n"
        f"• 🎯 {q_count} тест сұрағы\n\n"
        "👇 <b>Бөлімді таңдаңыз:</b>"
    )
    query.edit_message_text(text, parse_mode="HTML",
                             reply_markup=InlineKeyboardMarkup(keyboard))


# ─── Авторлар тізімі ────────────────────────────────────────────────────────

def show_authors_list(update: Update, context: CallbackContext, grade_num: int):
    query = update.callback_query
    query.answer()

    authors = _authors(grade_num)
    keyboard = []
    for key, author in authors.items():
        em = author.get("emoji", "👤")
        name = author.get("name", key)
        years = author.get("years", "")
        btn = f"{em} {name}"
        if years:
            btn += f" ({years})"
        keyboard.append([InlineKeyboardButton(btn, callback_data=f"enc_author_{grade_num}_{key}")])
    keyboard.append([InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")])

    grade = _grade(grade_num)
    em = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}.get(grade_num,"📖")
    title = grade.get("title", f"{grade_num}-сынып")

    query.edit_message_text(
        f"{em} <b>{title} — Авторлар</b>\n\n👨‍🏫 Авторды таңдаңыз:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── Автор толық профилі ────────────────────────────────────────────────────

def show_author_detail(update: Update, context: CallbackContext, grade_num: int, author_key: str):
    query = update.callback_query
    query.answer()

    author = _authors(grade_num).get(author_key)
    if not author:
        query.edit_message_text("❌ Автор табылмады")
        return

    name = author.get("name", "")
    years = author.get("years", "")
    born = author.get("born", "")
    em = author.get("emoji", "👤")
    bio = author.get("bio", "")
    facts = author.get("facts", [])
    works = author.get("works", [])
    quotes = author.get("quotes", [])

    text = f"{em} <b>{name}</b>"
    if years:
        text += f"  <i>{years}</i>"
    text += "\n\n"
    if born:
        text += f"🗺️ <b>Туған жері:</b> {born}\n\n"
    if bio:
        text += f"📝 <b>Өмірбаяны:</b>\n{bio}\n\n"
    if works:
        text += "📚 <b>Негізгі шығармалары:</b>\n"
        text += "\n".join(f"  • {w}" for w in works[:6])
        text += "\n\n"
    if facts:
        text += "💡 <b>Қызықты деректер:</b>\n"
        text += "\n".join(f"  ✓ {f}" for f in facts[:4])
        text += "\n\n"
    if quotes:
        text += "💬 <b>Дәйексөздер:</b>\n"
        text += "\n".join(f'  <i>"{q}"</i>' for q in quotes[:2])

    keyboard = [
        [InlineKeyboardButton("◀️ Авторлар", callback_data=f"enc_authors_{grade_num}")],
        [InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")],
    ]
    query.edit_message_text(text[:4000], parse_mode="HTML",
                             reply_markup=InlineKeyboardMarkup(keyboard))


# ─── Шығармалар тізімі ──────────────────────────────────────────────────────

def show_works_list(update: Update, context: CallbackContext, grade_num: int):
    query = update.callback_query
    query.answer()

    works = _works(grade_num)
    keyboard = []
    for key, work in works.items():
        name = work.get("name", key)
        genre = work.get("genre", "")
        btn = f"📖 {name}"
        if genre:
            btn += f" [{genre[:12]}]"
        keyboard.append([InlineKeyboardButton(btn, callback_data=f"enc_work_{grade_num}_{key}")])
    keyboard.append([InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")])

    grade = _grade(grade_num)
    em = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}.get(grade_num,"📖")
    title = grade.get("title", f"{grade_num}-сынып")

    query.edit_message_text(
        f"{em} <b>{title} — Шығармалар</b>\n\n📖 Шығарманы таңдаңыз:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── Шығарма толық профилі ─────────────────────────────────────────────────

def show_work_detail(update: Update, context: CallbackContext, grade_num: int, work_key: str):
    query = update.callback_query
    query.answer()

    work = _works(grade_num).get(work_key)
    if not work:
        query.edit_message_text("❌ Шығарма табылмады")
        return

    name = work.get("name", "")
    author = work.get("author", "")
    genre = work.get("genre", "")
    summary = work.get("summary", "")
    idea = work.get("idea", "")
    characters = work.get("characters", [])
    themes = work.get("themes", [])

    text = f"📖 <b>{name}</b>\n\n"
    if author:
        text += f"✍️ <b>Авторы:</b> {author}\n"
    if genre:
        text += f"📚 <b>Жанры:</b> {genre}\n"
    text += "\n"
    if summary:
        text += f"📝 <b>Қысқаша мазмұны:</b>\n{summary}\n\n"
    if idea:
        text += f"💡 <b>Негізгі идея:</b>\n<i>{idea}</i>\n\n"
    if characters:
        text += f"🎭 <b>Кейіпкерлер:</b> {', '.join(characters)}\n\n"
    if themes:
        text += f"🌟 <b>Тақырыптар:</b>\n" + " • ".join(themes)

    keyboard = [
        [InlineKeyboardButton("◀️ Шығармалар", callback_data=f"enc_works_{grade_num}")],
        [InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")],
    ]
    query.edit_message_text(text[:4000], parse_mode="HTML",
                             reply_markup=InlineKeyboardMarkup(keyboard))


# ─── Кейіпкерлер ───────────────────────────────────────────────────────────

def show_characters(update: Update, context: CallbackContext, grade_num: int):
    query = update.callback_query
    query.answer()

    chars = _characters(grade_num)
    grade = _grade(grade_num)
    em = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}.get(grade_num,"📖")
    title = grade.get("title", f"{grade_num}-сынып")

    text = f"{em} <b>{title} — Кейіпкерлер</b>\n\n"
    for key, char in chars.items():
        name = char.get("name", key)
        work = char.get("work", "")
        desc = char.get("desc", "")
        text += f"🎭 <b>{name}</b>"
        if work:
            text += f" — <i>{work}</i>"
        text += "\n"
        if desc:
            text += f"  {desc}\n"
        text += "\n"

    keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
    query.edit_message_text(text[:4000], parse_mode="HTML",
                             reply_markup=InlineKeyboardMarkup(keyboard))


# ─── Тақырыптар ────────────────────────────────────────────────────────────

def show_themes(update: Update, context: CallbackContext, grade_num: int):
    query = update.callback_query
    query.answer()

    themes = _themes(grade_num)
    grade = _grade(grade_num)
    em = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}.get(grade_num,"📖")
    title = grade.get("title", f"{grade_num}-сынып")

    text = f"{em} <b>{title} — Тақырыптар</b>\n\n"
    for i, theme in enumerate(themes, 1):
        text += f"{i}. {theme}\n"

    keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
    query.edit_message_text(text, parse_mode="HTML",
                             reply_markup=InlineKeyboardMarkup(keyboard))


# ─── Қызықты деректер ──────────────────────────────────────────────────────

def show_facts(update: Update, context: CallbackContext, grade_num: int):
    query = update.callback_query
    query.answer()

    facts = _facts(grade_num)
    grade = _grade(grade_num)
    em = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}.get(grade_num,"📖")
    title = grade.get("title", f"{grade_num}-сынып")

    text = f"{em} <b>{title} — Қызықты деректер</b>\n\n"
    for fact in facts:
        text += f"{fact}\n\n"

    keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
    query.edit_message_text(text[:4000], parse_mode="HTML",
                             reply_markup=InlineKeyboardMarkup(keyboard))


# ─── Терминдер сөздігі ──────────────────────────────────────────────────────

def show_terms(update: Update, context: CallbackContext, grade_num: int):
    query = update.callback_query
    query.answer()

    terms = _terms(grade_num)
    grade = _grade(grade_num)
    em = {1:"🌱",2:"🌿",3:"📗",4:"🌺",5:"🌟",6:"⚔️",7:"💎",8:"🦅",9:"✍️",10:"🔥",11:"🏆"}.get(grade_num,"📖")
    title = grade.get("title", f"{grade_num}-сынып")

    text = f"{em} <b>{title} — Терминдер сөздігі</b>\n\n"
    for key, definition in terms.items():
        if "—" in definition:
            parts = definition.split("—", 1)
            text += f"📌 <b>{parts[0].strip()}</b>\n  <i>{parts[1].strip()}</i>\n\n"
        else:
            text += f"📌 <b>{key}</b>\n  <i>{definition}</i>\n\n"

    keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
    query.edit_message_text(text[:4000], parse_mode="HTML",
                             reply_markup=InlineKeyboardMarkup(keyboard))


# ─── Тест — сұрақ ──────────────────────────────────────────────────────────

def show_quiz_question(update: Update, context: CallbackContext, grade_num: int, q_index: int):
    query = update.callback_query
    query.answer()

    quiz = _quiz(grade_num)
    if not quiz:
        keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
        query.edit_message_text("❌ Тест сұрақтары табылмады",
                                 reply_markup=InlineKeyboardMarkup(keyboard))
        return

    total = len(quiz)
    q_index = q_index % total
    q = quiz[q_index]

    question = q.get("q", "")
    options = q.get("opts", [])
    topic = q.get("topic", "")

    text = (
        f"🎯 <b>{grade_num}-сынып тесті</b> | {q_index + 1}/{total}\n"
        f"📌 Тақырып: <i>{topic}</i>\n\n"
        f"❓ {question}"
    )

    opts_emoji = ["🅰️", "🅱️", "🅲️", "🅳️"]
    keyboard = []
    for i, (opt, em) in enumerate(zip(options, opts_emoji)):
        keyboard.append([InlineKeyboardButton(
            f"{em} {opt}",
            callback_data=f"enc_qans_{grade_num}_{q_index}_{i}"
        )])

    nav = []
    if q_index > 0:
        nav.append(InlineKeyboardButton("◀️ Алдыңғы", callback_data=f"enc_quiz_{grade_num}_{q_index - 1}"))
    if q_index < total - 1:
        nav.append(InlineKeyboardButton("Келесі ▶️", callback_data=f"enc_quiz_{grade_num}_{q_index + 1}"))
    if nav:
        keyboard.append(nav)

    rand_idx = random.randint(0, total - 1)
    keyboard.append([
        InlineKeyboardButton("🔀 Кездейсоқ", callback_data=f"enc_quiz_{grade_num}_{rand_idx}"),
        InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}"),
    ])

    query.edit_message_text(text, parse_mode="HTML",
                             reply_markup=InlineKeyboardMarkup(keyboard))


# ─── Тест — жауап ──────────────────────────────────────────────────────────

def show_quiz_answer(update: Update, context: CallbackContext, grade_num: int, q_index: int, chosen_idx: int):
    query = update.callback_query
    query.answer()

    quiz = _quiz(grade_num)
    if not quiz or q_index >= len(quiz):
        return

    total = len(quiz)
    q = quiz[q_index]
    question = q.get("q", "")
    options = q.get("opts", [])
    correct_idx = q.get("ai", 0)
    topic = q.get("topic", "")
    correct_ans = options[correct_idx] if correct_idx < len(options) else ""

    is_correct = (chosen_idx == correct_idx)

    if is_correct:
        result = "✅ <b>Дұрыс! Керемет!</b>"
    else:
        result = f"❌ Дұрыс жауап: <b>{correct_ans}</b>"

    text = (
        f"🎯 <b>{grade_num}-сынып тесті</b> | {q_index + 1}/{total}\n"
        f"📌 Тақырып: <i>{topic}</i>\n\n"
        f"❓ {question}\n\n"
        f"{result}\n\n"
    )

    for i, opt in enumerate(options):
        if i == correct_idx:
            text += f"✅ {opt}\n"
        elif i == chosen_idx and not is_correct:
            text += f"❌ {opt}\n"
        else:
            text += f"◻️ {opt}\n"

    keyboard = []
    nav = []
    if q_index > 0:
        nav.append(InlineKeyboardButton("◀️ Алдыңғы", callback_data=f"enc_quiz_{grade_num}_{q_index - 1}"))
    if q_index < total - 1:
        nav.append(InlineKeyboardButton("Келесі ▶️", callback_data=f"enc_quiz_{grade_num}_{q_index + 1}"))
    if nav:
        keyboard.append(nav)
    keyboard.append([InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")])

    query.edit_message_text(text, parse_mode="HTML",
                             reply_markup=InlineKeyboardMarkup(keyboard))


# ─── Маршруттаушы (синхронды) ───────────────────────────────────────────────

def encyclopedia_callback_handler(update: Update, context: CallbackContext):
    """Барлық enc_ callback'тарды маршруттайды — синхронды PTB v13 нұсқасы"""
    query = update.callback_query
    data = query.data

    try:
        if data == "encyclopedia":
            show_encyclopedia_menu(update, context)

        elif data.startswith("enc_grade_"):
            g = int(data.split("_")[2])
            show_grade_menu(update, context, g)

        elif data.startswith("enc_authors_"):
            g = int(data.split("_")[2])
            show_authors_list(update, context, g)

        elif data.startswith("enc_author_"):
            parts = data.split("_")
            g = int(parts[2])
            key = "_".join(parts[3:])
            show_author_detail(update, context, g, key)

        elif data.startswith("enc_works_"):
            g = int(data.split("_")[2])
            show_works_list(update, context, g)

        elif data.startswith("enc_work_"):
            parts = data.split("_")
            g = int(parts[2])
            key = "_".join(parts[3:])
            show_work_detail(update, context, g, key)

        elif data.startswith("enc_chars_"):
            g = int(data.split("_")[2])
            show_characters(update, context, g)

        elif data.startswith("enc_themes_"):
            g = int(data.split("_")[2])
            show_themes(update, context, g)

        elif data.startswith("enc_facts_"):
            g = int(data.split("_")[2])
            show_facts(update, context, g)

        elif data.startswith("enc_terms_"):
            g = int(data.split("_")[2])
            show_terms(update, context, g)

        elif data.startswith("enc_quiz_"):
            parts = data.split("_")
            g = int(parts[2])
            q_idx = int(parts[3])
            show_quiz_question(update, context, g, q_idx)

        elif data.startswith("enc_qans_"):
            parts = data.split("_")
            g = int(parts[2])
            q_idx = int(parts[3])
            chosen = int(parts[4])
            show_quiz_answer(update, context, g, q_idx, chosen)

    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Encyclopedia error [{data}]: {e}")
        try:
            query.edit_message_text(
                f"❌ Қате орын алды. Артқа оралып, қайталаңыз.\n<code>{str(e)[:80]}</code>",
                parse_mode="HTML"
            )
        except Exception:
            pass
