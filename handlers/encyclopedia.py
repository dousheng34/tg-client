"""
handlers/encyclopedia.py
Визуалды энциклопедия handler — 1-11 сынып
Тарау → Автор → Шығарма → Кейіпкер → Сұрақ-жауап
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import random

try:
    from content.encyclopedia import ENCYCLOPEDIA, get_grade, get_authors, get_works, get_characters, get_themes, get_facts, get_terms, all_grades
    from content.quiz_bank import QUIZ_BANK, get_quiz, count_questions
except ImportError:
    ENCYCLOPEDIA = {}
    QUIZ_BANK = {}
    def get_grade(g): return {}
    def get_authors(g): return {}
    def get_works(g): return {}
    def get_characters(g): return {}
    def get_themes(g): return []
    def get_facts(g): return []
    def get_terms(g): return {}
    def get_quiz(g): return []
    def all_grades(): return []
    def count_questions(g): return 0

# ─── Сынып мәзірі ─────────────────────────────────────────────────────────

async def show_encyclopedia_menu(update: Update, context: CallbackContext):
    """Визуалды Энциклопедия — бас мәзір"""
    query = update.callback_query
    if query:
        await query.answer()

    keyboard = []
    for grade_num in range(1, 12):
        grade = get_grade(grade_num)
        if grade:
            emoji = grade.get("emoji", "📖")
            title = grade.get("title", f"{grade_num}-сынып")
            keyboard.append([InlineKeyboardButton(
                f"{emoji} {title}",
                callback_data=f"enc_grade_{grade_num}"
            )])
    keyboard.append([InlineKeyboardButton("🏠 Басты мәзір", callback_data="main_menu")])

    text = (
        "📚 *Қазақ Әдебиеті — Визуалды Энциклопедия*\n\n"
        "🎓 1-11 сынып бойынша толыq контент:\n"
        "• 👨‍🏫 Авторлар өмірбаяны\n"
        "• 📖 Шығармалар талдауы\n"
        "• 🎭 Кейіпкерлер сипаты\n"
        "• 💡 Қызықты деректер\n"
        "• 📝 Тест сұрақтары\n"
        "• 📑 Әдебиет терминдері\n\n"
        "👇 *Сыныпты таңдаңыз:*"
    )

    markup = InlineKeyboardMarkup(keyboard)

    if query:
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=markup)
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=markup)


# ─── Сынып бөлімдері ─────────────────────────────────────────────────────

async def show_grade_sections(update: Update, context: CallbackContext, grade_num: int):
    """Бір сынып үшін бөлімдер мәзірі"""
    query = update.callback_query
    if query:
        await query.answer()

    grade = get_grade(grade_num)
    if not grade:
        await query.edit_message_text("❌ Мазмұн табылмады")
        return

    emoji = grade.get("emoji", "📖")
    title = grade.get("title", f"{grade_num}-сынып")

    authors_count = len(get_authors(grade_num))
    works_count = len(get_works(grade_num))
    chars_count = len(get_characters(grade_num))
    themes_count = len(get_themes(grade_num))
    facts_count = len(get_facts(grade_num))
    terms_count = len(get_terms(grade_num))
    quiz_count = count_questions(grade_num)

    keyboard = [
        [InlineKeyboardButton(f"👨‍🏫 Авторлар ({authors_count})", callback_data=f"enc_authors_{grade_num}")],
        [InlineKeyboardButton(f"📖 Шығармалар ({works_count})", callback_data=f"enc_works_{grade_num}")],
        [InlineKeyboardButton(f"🎭 Кейіпкерлер ({chars_count})", callback_data=f"enc_chars_{grade_num}")],
        [InlineKeyboardButton(f"🌟 Тақырыптар ({themes_count})", callback_data=f"enc_themes_{grade_num}")],
        [InlineKeyboardButton(f"💡 Қызықты деректер ({facts_count})", callback_data=f"enc_facts_{grade_num}")],
        [InlineKeyboardButton(f"📑 Терминдер сөздігі ({terms_count})", callback_data=f"enc_terms_{grade_num}")],
        [InlineKeyboardButton(f"🎯 Тест сұрақтары ({quiz_count})", callback_data=f"enc_quiz_{grade_num}_0")],
        [InlineKeyboardButton("◀️ Сыныптар тізімі", callback_data="encyclopedia")],
    ]

    text = (
        f"{emoji} *{title}*\n\n"
        f"📚 Барлық материалдар:\n"
        f"• 👨‍🏫 Авторлар: {authors_count} тұлға\n"
        f"• 📖 Шығармалар: {works_count} туынды\n"
        f"• 🎭 Кейіпкерлер: {chars_count} образ\n"
        f"• 🌟 Тақырыптар: {themes_count}\n"
        f"• 💡 Деректер: {facts_count}\n"
        f"• 📑 Терминдер: {terms_count}\n"
        f"• 🎯 Тест сұрақтары: {quiz_count}\n\n"
        f"👇 *Бөлімді таңдаңыз:*"
    )

    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=markup)


# ─── Авторлар тізімі ────────────────────────────────────────────────────────

async def show_authors_list(update: Update, context: CallbackContext, grade_num: int):
    """Авторлар тізімі"""
    query = update.callback_query
    if query:
        await query.answer()

    authors = get_authors(grade_num)
    if not authors:
        await query.edit_message_text("❌ Авторлар табылмады")
        return

    keyboard = []
    for key, author in authors.items():
        emoji = author.get("emoji", "👤")
        name = author.get("name", key)
        years = author.get("years", "")
        btn_text = f"{emoji} {name}"
        if years:
            btn_text += f" ({years})"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"enc_author_{grade_num}_{key}")])

    keyboard.append([InlineKeyboardButton(f"◀️ {grade_num}-сынып мәзірі", callback_data=f"enc_grade_{grade_num}")])

    grade = get_grade(grade_num)
    emoji = grade.get("emoji", "📖")
    title = grade.get("title", f"{grade_num}-сынып")

    text = f"{emoji} *{title} — Авторлар*\n\n👨‍🏫 Авторды таңдаңыз:"
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=markup)


# ─── Автор толық профилі ────────────────────────────────────────────────────

async def show_author_detail(update: Update, context: CallbackContext, grade_num: int, author_key: str):
    """Авторды толық ақпараттарымен көрсету"""
    query = update.callback_query
    if query:
        await query.answer()

    authors = get_authors(grade_num)
    author = authors.get(author_key)
    if not author:
        await query.edit_message_text("❌ Автор табылмады")
        return

    name = author.get("name", "")
    years = author.get("years", "")
    born = author.get("born", "")
    emoji = author.get("emoji", "👤")
    bio = author.get("bio", "")
    facts = author.get("facts", [])
    works = author.get("works", [])
    quotes = author.get("quotes", [])

    text = f"{emoji} *{name}*"
    if years:
        text += f" _{years}_"
    text += "\n\n"

    if born:
        text += f"🗺️ *Туған жері:* {born}\n\n"

    if bio:
        text += f"📝 *Өмірбаян:*\n{bio}\n\n"

    if works:
        text += f"📚 *Негізгі шығармалары:*\n"
        text += "\n".join(f"  • {w}" for w in works[:6])
        text += "\n\n"

    if facts:
        text += f"💡 *Қызықты деректер:*\n"
        text += "\n".join(f"  ✓ {f}" for f in facts[:4])
        text += "\n\n"

    if quotes:
        text += f"💬 *Дәйексөздер:*\n"
        text += "\n".join(f"  _\"{q}\"_" for q in quotes[:2])

    keyboard = [
        [InlineKeyboardButton("◀️ Авторлар тізімі", callback_data=f"enc_authors_{grade_num}")],
        [InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")],
    ]

    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text[:4000], parse_mode="Markdown", reply_markup=markup)


# ─── Шығармалар тізімі ──────────────────────────────────────────────────────

async def show_works_list(update: Update, context: CallbackContext, grade_num: int):
    """Шығармалар тізімі"""
    query = update.callback_query
    if query:
        await query.answer()

    works = get_works(grade_num)
    if not works:
        await query.edit_message_text("❌ Шығармалар табылмады")
        return

    keyboard = []
    for key, work in works.items():
        name = work.get("name", key)
        author = work.get("author", "")
        genre = work.get("genre", "")
        btn_text = f"📖 {name}"
        if genre:
            btn_text += f" [{genre[:15]}]"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"enc_work_{grade_num}_{key}")])

    keyboard.append([InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")])

    grade = get_grade(grade_num)
    emoji = grade.get("emoji", "📖")
    title = grade.get("title", f"{grade_num}-сынып")

    text = f"{emoji} *{title} — Шығармалар*\n\n📖 Шығарманы таңдаңыз:"
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=markup)


# ─── Шығарма толық профилі ─────────────────────────────────────────────────

async def show_work_detail(update: Update, context: CallbackContext, grade_num: int, work_key: str):
    """Шығарманы толық ақпараттарымен көрсету"""
    query = update.callback_query
    if query:
        await query.answer()

    works = get_works(grade_num)
    work = works.get(work_key)
    if not work:
        await query.edit_message_text("❌ Шығарма табылмады")
        return

    name = work.get("name", "")
    author = work.get("author", "")
    genre = work.get("genre", "")
    summary = work.get("summary", "")
    idea = work.get("idea", "")
    characters = work.get("characters", [])
    themes = work.get("themes", [])

    text = f"📖 *{name}*\n\n"

    if author:
        text += f"✍️ *Авторы:* {author}\n"
    if genre:
        text += f"📚 *Жанры:* {genre}\n"
    text += "\n"

    if summary:
        text += f"📝 *Қысқаша мазмұны:*\n{summary}\n\n"

    if idea:
        text += f"💡 *Негізгі идея:*\n_{idea}_\n\n"

    if characters:
        text += f"🎭 *Кейіпкерлер:*\n"
        text += ", ".join(f"_{c}_" for c in characters)
        text += "\n\n"

    if themes:
        text += f"🌟 *Тақырыптар:*\n"
        text += " • ".join(themes)

    keyboard = [
        [InlineKeyboardButton("◀️ Шығармалар тізімі", callback_data=f"enc_works_{grade_num}")],
        [InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")],
    ]

    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text[:4000], parse_mode="Markdown", reply_markup=markup)


# ─── Кейіпкерлер ───────────────────────────────────────────────────────────

async def show_characters(update: Update, context: CallbackContext, grade_num: int):
    """Кейіпкерлер тізімі"""
    query = update.callback_query
    if query:
        await query.answer()

    chars = get_characters(grade_num)
    grade = get_grade(grade_num)
    emoji = grade.get("emoji", "📖")
    title = grade.get("title", f"{grade_num}-сынып")

    if not chars:
        keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
        await query.edit_message_text("❌ Кейіпкерлер табылмады", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    text = f"{emoji} *{title} — Кейіпкерлер*\n\n"

    for key, char in chars.items():
        name = char.get("name", key)
        work = char.get("work", "")
        desc = char.get("desc", "")

        text += f"🎭 *{name}*"
        if work:
            text += f" — _{work}_"
        text += "\n"
        if desc:
            text += f"  {desc}\n"
        text += "\n"

    keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text[:4000], parse_mode="Markdown", reply_markup=markup)


# ─── Тақырыптар ────────────────────────────────────────────────────────────

async def show_themes(update: Update, context: CallbackContext, grade_num: int):
    """Тақырыптар тізімі"""
    query = update.callback_query
    if query:
        await query.answer()

    themes = get_themes(grade_num)
    grade = get_grade(grade_num)
    emoji = grade.get("emoji", "📖")
    title = grade.get("title", f"{grade_num}-сынып")

    text = f"{emoji} *{title} — Тақырыптар*\n\n"
    for i, theme in enumerate(themes, 1):
        text += f"{i}. {theme}\n"

    keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=markup)


# ─── Қызықты деректер ──────────────────────────────────────────────────────

async def show_facts(update: Update, context: CallbackContext, grade_num: int):
    """Қызықты деректер"""
    query = update.callback_query
    if query:
        await query.answer()

    facts = get_facts(grade_num)
    grade = get_grade(grade_num)
    emoji = grade.get("emoji", "📖")
    title = grade.get("title", f"{grade_num}-сынып")

    text = f"{emoji} *{title} — Қызықты деректер*\n\n"
    for fact in facts:
        text += f"{fact}\n\n"

    keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text[:4000], parse_mode="Markdown", reply_markup=markup)


# ─── Терминдер сөздігі ──────────────────────────────────────────────────────

async def show_terms(update: Update, context: CallbackContext, grade_num: int):
    """Терминдер сөздігі"""
    query = update.callback_query
    if query:
        await query.answer()

    terms = get_terms(grade_num)
    grade = get_grade(grade_num)
    emoji = grade.get("emoji", "📖")
    title = grade.get("title", f"{grade_num}-сынып")

    text = f"{emoji} *{title} — Терминдер сөздігі*\n\n"
    for key, definition in terms.items():
        text += f"📌 *{definition.split('—')[0].strip()}*\n"
        if "—" in definition:
            text += f"  _{definition.split('—', 1)[1].strip()}_\n\n"
        else:
            text += f"  _{definition}_\n\n"

    keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text[:4000], parse_mode="Markdown", reply_markup=markup)


# ─── Тест сұрақтары ─────────────────────────────────────────────────────────

async def show_quiz_question(update: Update, context: CallbackContext, grade_num: int, q_index: int):
    """Тест сұрағын көрсету"""
    query = update.callback_query
    if query:
        await query.answer()

    quiz = get_quiz(grade_num)
    if not quiz:
        keyboard = [[InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}")]]
        await query.edit_message_text("❌ Тест сұрақтары табылмады", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    q_index = q_index % len(quiz)
    q = quiz[q_index]

    question = q.get("q", "")
    options = q.get("opts", [])
    correct_idx = q.get("ai", 0)
    topic = q.get("topic", "")
    total = len(quiz)

    text = (
        f"🎯 *{grade_num}-сынып тесті* | Сұрақ {q_index + 1}/{total}\n"
        f"📌 Тақырып: _{topic}_\n\n"
        f"❓ {question}"
    )

    keyboard = []
    opts_emoji = ["🅰️", "🅱️", "🅲️", "🅳️"]
    for i, (opt, em) in enumerate(zip(options, opts_emoji)):
        keyboard.append([InlineKeyboardButton(
            f"{em} {opt}",
            callback_data=f"enc_qans_{grade_num}_{q_index}_{i}"
        )])

    # Навигация
    nav = []
    if q_index > 0:
        nav.append(InlineKeyboardButton("◀️", callback_data=f"enc_quiz_{grade_num}_{q_index - 1}"))
    if q_index < total - 1:
        nav.append(InlineKeyboardButton("▶️", callback_data=f"enc_quiz_{grade_num}_{q_index + 1}"))
    if nav:
        keyboard.append(nav)

    keyboard.append([
        InlineKeyboardButton("🔀 Кездейсоқ", callback_data=f"enc_quiz_{grade_num}_{random.randint(0, total-1)}"),
        InlineKeyboardButton(f"◀️ {grade_num}-сынып", callback_data=f"enc_grade_{grade_num}"),
    ])

    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=markup)


# ─── Тест жауабы ─────────────────────────────────────────────────────────────

async def show_quiz_answer(update: Update, context: CallbackContext, grade_num: int, q_index: int, chosen_idx: int):
    """Таңдалған жауапты тексеру"""
    query = update.callback_query
    if query:
        await query.answer()

    quiz = get_quiz(grade_num)
    if not quiz or q_index >= len(quiz):
        return

    q = quiz[q_index]
    question = q.get("q", "")
    options = q.get("opts", [])
    correct_idx = q.get("ai", 0)
    topic = q.get("topic", "")
    correct_ans = q.get("a", options[correct_idx] if correct_idx < len(options) else "")
    total = len(quiz)

    is_correct = chosen_idx == correct_idx

    if is_correct:
        result_emoji = "✅"
        result_text = "Дұрыс! Керемет!"
    else:
        result_emoji = "❌"
        result_text = f"Дұрыс жауап: *{correct_ans}*"

    text = (
        f"🎯 *{grade_num}-сынып тесті* | Сұрақ {q_index + 1}/{total}\n"
        f"📌 Тақырып: _{topic}_\n\n"
        f"❓ {question}\n\n"
        f"{result_emoji} {result_text}\n\n"
    )

    # Барлық орардарды белгілеу
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

    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=markup)


# ─── Callback router ─────────────────────────────────────────────────────────

async def encyclopedia_callback_handler(update: Update, context: CallbackContext):
    """Барлық энциклопедия callback'тарды маршруттайды"""
    query = update.callback_query
    data = query.data

    try:
        if data == "encyclopedia":
            await show_encyclopedia_menu(update, context)

        elif data.startswith("enc_grade_"):
            grade_num = int(data.split("_")[2])
            await show_grade_sections(update, context, grade_num)

        elif data.startswith("enc_authors_"):
            grade_num = int(data.split("_")[2])
            await show_authors_list(update, context, grade_num)

        elif data.startswith("enc_author_"):
            parts = data.split("_")
            grade_num = int(parts[2])
            author_key = "_".join(parts[3:])
            await show_author_detail(update, context, grade_num, author_key)

        elif data.startswith("enc_works_"):
            grade_num = int(data.split("_")[2])
            await show_works_list(update, context, grade_num)

        elif data.startswith("enc_work_"):
            parts = data.split("_")
            grade_num = int(parts[2])
            work_key = "_".join(parts[3:])
            await show_work_detail(update, context, grade_num, work_key)

        elif data.startswith("enc_chars_"):
            grade_num = int(data.split("_")[2])
            await show_characters(update, context, grade_num)

        elif data.startswith("enc_themes_"):
            grade_num = int(data.split("_")[2])
            await show_themes(update, context, grade_num)

        elif data.startswith("enc_facts_"):
            grade_num = int(data.split("_")[2])
            await show_facts(update, context, grade_num)

        elif data.startswith("enc_terms_"):
            grade_num = int(data.split("_")[2])
            await show_terms(update, context, grade_num)

        elif data.startswith("enc_quiz_"):
            parts = data.split("_")
            grade_num = int(parts[2])
            q_index = int(parts[3])
            await show_quiz_question(update, context, grade_num, q_index)

        elif data.startswith("enc_qans_"):
            parts = data.split("_")
            grade_num = int(parts[2])
            q_index = int(parts[3])
            chosen_idx = int(parts[4])
            await show_quiz_answer(update, context, grade_num, q_index, chosen_idx)

    except Exception as e:
        print(f"Encyclopedia handler error: {e}")
        try:
            await query.edit_message_text(f"❌ Қате: {str(e)[:100]}")
        except:
            pass
