"""handlers/quiz.py — Викторина мен барлық ойын түрлері"""
import random
from telegram import Update
from telegram.ext import CallbackContext
from content.quizzes import (
    get_quizzes_for_grade, get_random_quizzes,
    get_quote_match, get_work_author_match,
    get_character_quizzes, get_blitz
)
from database import add_points, save_game_result, give_achievement, get_or_create_user
from utils.keyboards import (
    quiz_answer_keyboard, next_question_keyboard,
    game_result_keyboard, games_keyboard, grade_select_for_game_keyboard
)

LETTERS = ["🅰️", "🅱️", "🅲️", "🅳️"]

# ── Ойындар хабы ────────────────────────────────────────────────────────────────
def games_menu_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "🎮 <b>ОЙЫНДАР</b>\n\n"
        "Ойын түрін таңдаңыз:\n\n"
        "🎯 <b>Викторина</b> — 4 нұсқалы сұрақтар\n"
        "✍️ <b>Кім жазды?</b> — шығарманың авторын тап\n"
        "📚 <b>Шығарманы тап!</b> — сипаттамасы бойынша\n"
        "💬 <b>Цитата жарысы</b> — цитатаны авторға сай\n"
        "⚡ <b>Блиц-тур</b> — жылдам жауап\n"
        "👥 <b>Кейіпкерлер</b> — кейіпкерді тап",
        parse_mode='HTML',
        reply_markup=games_menu_kb()
    )

def games_menu_kb():
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 Викторина", callback_data="game_quiz"),
         InlineKeyboardButton("✍️ Кім жазды?", callback_data="game_whowrote")],
        [InlineKeyboardButton("📚 Шығарманы тап!", callback_data="game_findwork"),
         InlineKeyboardButton("💬 Цитата жарысы", callback_data="game_quote")],
        [InlineKeyboardButton("⚡ Блиц-тур", callback_data="game_blitz"),
         InlineKeyboardButton("👥 Кейіпкерлер", callback_data="game_character")],
        [InlineKeyboardButton("🔙 Артқа", callback_data="menu_main")],
    ])

# ── Ойын сынып таңдау ───────────────────────────────────────────────────────────
def game_quiz_start(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "🎯 <b>ВИКТОРИНА</b>\n\nҚай сынып материалы бойынша ойнайсыз?",
        parse_mode='HTML',
        reply_markup=grade_select_for_game_keyboard("quiz")
    )

def game_whowrote_start(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "✍️ <b>КІМ ЖАЗДЫ?</b>\n\nШығарма берілмейді — авторы сұралады!\nҚай сынып?",
        parse_mode='HTML',
        reply_markup=grade_select_for_game_keyboard("whowrote")
    )

def game_findwork_start(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "📚 <b>ШЫҒАРМАНЫ ТАП!</b>\n\nАвтор берілмейді — шығармасы сұралады!\nҚай сынып?",
        parse_mode='HTML',
        reply_markup=grade_select_for_game_keyboard("findwork")
    )

def game_quote_start(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    _start_quote_game(query, context)

def game_blitz_start(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    _start_blitz_game(query, context)

def game_character_start(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    _start_character_game(query, context)

# ── Сынып таңдалғаннан кейін ойын басталады ────────────────────────────────────
def game_grade_selected(update: Update, context: CallbackContext):
    """callback_data = game_{type}_grade_{g}"""
    query = update.callback_query
    query.answer()
    parts = query.data.split('_')
    # game_{type}_grade_{g} → parts[1]=type, parts[-1]=grade
    grade = int(parts[-1])
    game_type = parts[1]

    if game_type == "quiz":
        questions = get_quizzes_for_grade(grade, 10) if grade > 0 else get_random_quizzes(10)
        _start_quiz(query, context, questions, "quiz", grade)
    elif game_type == "whowrote":
        questions = get_work_author_match(8)
        _start_work_author(query, context, questions, "whowrote", grade)
    elif game_type == "findwork":
        questions = get_work_author_match(8)
        _start_findwork(query, context, questions, "findwork", grade)

# ══ ВИКТОРИНА ════════════════════════════════════════════════════════════════════
def _start_quiz(query, context, questions, game_type, grade):
    context.user_data['quiz'] = {
        'questions': questions,
        'current': 0,
        'score': 0,
        'total': len(questions),
        'game_type': game_type,
        'grade': grade,
        'answered': False,
    }
    _send_quiz_question(query, context)


def _send_quiz_question(query, context):
    qd = context.user_data.get('quiz', {})
    idx = qd['current']
    questions = qd['questions']
    if idx >= len(questions):
        _end_quiz(query, context)
        return
    q = questions[idx]
    opts = q['opts'].copy()
    random.shuffle(opts)
    # Жауап нұсқаларын сақта
    qd['current_opts'] = opts
    qd['correct_answer'] = q['a']
    qd['answered'] = False

    num = idx + 1
    total = qd['total']
    score = qd['score']
    text = (
        f"🎯 <b>Сұрақ {num}/{total}</b>   ✅ {score} дұрыс\n\n"
        f"❓ <b>{q['q']}</b>"
    )
    kb = quiz_answer_keyboard(opts)
    try:
        query.edit_message_text(text, parse_mode='HTML', reply_markup=kb)
    except Exception:
        pass


def quiz_answer_callback(update: Update, context: CallbackContext):
    """Жауап берілді"""
    query = update.callback_query
    qd = context.user_data.get('quiz')
    if not qd or qd.get('answered'):
        query.answer()
        return

    idx = int(query.data.split('_')[1])
    opts = qd.get('current_opts', [])
    correct = qd.get('correct_answer', '')
    selected = opts[idx] if idx < len(opts) else ''

    is_correct = (selected == correct)
    qd['answered'] = True

    if is_correct:
        qd['score'] += 1
        query.answer("✅ Дұрыс! +10 ұпай", show_alert=False)
        add_points(update.effective_user.id, 10)
    else:
        query.answer(f"❌ Қате! Дұрыс жауап: {correct}", show_alert=True)

    kb = quiz_answer_keyboard(opts, correct, selected)
    num = qd['current'] + 1
    total = qd['total']
    score = qd['score']
    status = "✅ Дұрыс!" if is_correct else f"❌ Қате! Жауап: {correct}"

    text = (
        f"🎯 <b>Сұрақ {num}/{total}</b>   ✅ {score} дұрыс\n\n"
        f"❓ <b>{context.user_data['quiz']['questions'][qd['current']]['q']}</b>\n\n"
        f"{status}"
    )
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    next_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ Келесі сұрақ", callback_data="quiz_next")],
        [InlineKeyboardButton("🛑 Тоқтату", callback_data="quiz_stop")],
    ])
    try:
        query.edit_message_text(text, parse_mode='HTML', reply_markup=next_kb)
    except Exception:
        pass


def quiz_next_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    qd = context.user_data.get('quiz')
    if not qd:
        query.edit_message_text("Ойын жоқ.", reply_markup=game_result_keyboard())
        return
    qd['current'] += 1
    if qd['current'] >= qd['total']:
        _end_quiz(query, context)
    else:
        _send_quiz_question(query, context)


def quiz_stop_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    _end_quiz(query, context)


def _end_quiz(query, context):
    qd = context.user_data.get('quiz', {})
    score = qd.get('score', 0)
    total = qd.get('total', 10)
    game_type = qd.get('game_type', 'quiz')
    grade = qd.get('grade', 0)
    user_id = query.from_user.id

    save_game_result(user_id, game_type, score, total, grade)

    # Бонус бар ма?
    bonus = ""
    if score == total and total > 0:
        add_points(user_id, 50)
        give_achievement(user_id, 'perfect_quiz')
        bonus = "\n🏆 <b>Мінсіз нәтиже! +50 бонус ұпай!</b>"

    # Жетістік тексеру
    from database import get_user_stats
    stats = get_user_stats(user_id)
    games = stats.get('total_games', 0)
    if games >= 1:
        give_achievement(user_id, 'first_game')
    if games >= 10:
        give_achievement(user_id, 'games_10')

    percent = int(score / total * 100) if total > 0 else 0
    if percent >= 90:
        result_emoji = "🏆"
        result_text = "Керемет нәтиже!"
    elif percent >= 70:
        result_emoji = "🌟"
        result_text = "Жақсы нәтиже!"
    elif percent >= 50:
        result_emoji = "👍"
        result_text = "Орташа нәтиже."
    else:
        result_emoji = "📚"
        result_text = "Оқуды жалғастыр!"

    text = (
        f"{result_emoji} <b>ОЙЫН АЯҚТАЛДЫ!</b>\n\n"
        f"✅ Дұрыс жауап: <b>{score}/{total}</b> ({percent}%)\n"
        f"💬 {result_text}{bonus}\n\n"
        f"📊 Жалпы ұпайыңды профильден қара!"
    )
    context.user_data.pop('quiz', None)
    try:
        query.edit_message_text(text, parse_mode='HTML', reply_markup=game_result_keyboard())
    except Exception:
        pass


# ══ КІМ ЖАЗДЫ? (Шығарма → Автор) ════════════════════════════════════════════════
def _start_work_author(query, context, questions, game_type, grade):
    context.user_data['wa_game'] = {
        'questions': questions,
        'current': 0,
        'score': 0,
        'total': len(questions),
        'game_type': game_type,
        'grade': grade,
        'answered': False,
    }
    _send_wa_question(query, context)


def _send_wa_question(query, context):
    qd = context.user_data.get('wa_game', {})
    idx = qd['current']
    questions = qd['questions']
    if idx >= len(questions):
        _end_wa_game(query, context)
        return
    q = questions[idx]
    opts = q['opts'].copy()
    random.shuffle(opts)
    qd['wa_opts'] = opts
    qd['wa_correct'] = q['author']
    qd['answered'] = False

    num = idx + 1
    total = qd['total']
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    buttons = [[InlineKeyboardButton(f"{LETTERS[i]} {opt}", callback_data=f"wa_ans_{i}")]
               for i, opt in enumerate(opts)]
    kb = InlineKeyboardMarkup(buttons)
    text = (
        f"✍️ <b>КІМ ЖАЗДЫ? {num}/{total}</b>\n\n"
        f"📗 Шығарма: <b>{q['work']}</b>\n\n"
        f"Авторды таңдаңыз:"
    )
    try:
        query.edit_message_text(text, parse_mode='HTML', reply_markup=kb)
    except Exception:
        pass


def wa_answer_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    qd = context.user_data.get('wa_game')
    if not qd or qd.get('answered'):
        query.answer()
        return
    idx = int(query.data.split('_')[-1])
    opts = qd.get('wa_opts', [])
    correct = qd.get('wa_correct', '')
    selected = opts[idx] if idx < len(opts) else ''
    is_correct = (selected == correct)
    qd['answered'] = True
    if is_correct:
        qd['score'] += 1
        query.answer("✅ Дұрыс!", show_alert=False)
        add_points(update.effective_user.id, 10)
    else:
        query.answer(f"❌ Дұрыс: {correct}", show_alert=True)
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    next_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ Келесі", callback_data="wa_next")],
        [InlineKeyboardButton("🛑 Тоқтату", callback_data="wa_stop")],
    ])
    status = "✅ Дұрыс!" if is_correct else f"❌ Дұрыс жауап: <b>{correct}</b>"
    q = qd['questions'][qd['current']]
    try:
        query.edit_message_text(
            f"✍️ <b>КІМ ЖАЗДЫ?</b>\n\n📗 {q['work']}\n\n{status}",
            parse_mode='HTML', reply_markup=next_kb)
    except Exception:
        pass


def wa_next_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    qd = context.user_data.get('wa_game')
    if not qd:
        return
    qd['current'] += 1
    if qd['current'] >= qd['total']:
        _end_wa_game(query, context)
    else:
        _send_wa_question(query, context)


def wa_stop_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    _end_wa_game(query, context)


def _end_wa_game(query, context):
    qd = context.user_data.get('wa_game', {})
    score = qd.get('score', 0)
    total = qd.get('total', 0)
    save_game_result(query.from_user.id, qd.get('game_type','whowrote'), score, total)
    percent = int(score / total * 100) if total else 0
    context.user_data.pop('wa_game', None)
    try:
        query.edit_message_text(
            f"✍️ <b>КІМ ЖАЗДЫ? — АЯҚТАЛДЫ!</b>\n\n"
            f"✅ Дұрыс: <b>{score}/{total}</b> ({percent}%)",
            parse_mode='HTML', reply_markup=game_result_keyboard())
    except Exception:
        pass


# ══ ШЫҒАРМАНЫ ТАП (Автор → Шығарма) ═════════════════════════════════════════════
def _start_findwork(query, context, questions, game_type, grade):
    # Сұрақтарды авторынан шығармасын тапқызу форматына айналдыр
    fw_q = []
    from content.quizzes import WORK_AUTHOR_MATCH
    import random
    pool = WORK_AUTHOR_MATCH.copy()
    random.shuffle(pool)
    for item in pool[:8]:
        all_works = [x['work'] for x in WORK_AUTHOR_MATCH]
        wrong = [w for w in all_works if w != item['work']]
        random.shuffle(wrong)
        opts = [item['work']] + wrong[:3]
        random.shuffle(opts)
        fw_q.append({
            'q': f"Авторы: {item['author']}",
            'a': item['work'],
            'opts': opts
        })
    context.user_data['quiz'] = {
        'questions': fw_q,
        'current': 0,
        'score': 0,
        'total': len(fw_q),
        'game_type': 'findwork',
        'grade': grade,
        'answered': False,
    }
    _send_quiz_question(query, context)


# ══ ЦИТАТА ЖАРЫСЫ ═════════════════════════════════════════════════════════════════
def _start_quote_game(query, context):
    questions = get_quote_match(8)
    qdata = []
    for q in questions:
        opts = q['opts'].copy()
        random.shuffle(opts)
        qdata.append({'q': q['quote'], 'a': q['author'], 'opts': opts})
    context.user_data['quiz'] = {
        'questions': qdata,
        'current': 0,
        'score': 0,
        'total': len(qdata),
        'game_type': 'quote',
        'grade': 0,
        'answered': False,
    }
    _send_quiz_question(query, context)


# ══ БЛИЦ-ТУР ══════════════════════════════════════════════════════════════════════
def _start_blitz_game(query, context):
    questions = get_blitz(10)
    qdata = []
    from content.authors import AUTHORS
    all_names = [v['name'].split()[0] for v in AUTHORS.values()]
    for q in questions:
        wrong = [n for n in all_names if n != q['a']]
        random.shuffle(wrong)
        opts = [q['a']] + wrong[:3]
        random.shuffle(opts)
        qdata.append({'q': q['q'], 'a': q['a'], 'opts': opts})
    context.user_data['quiz'] = {
        'questions': qdata,
        'current': 0,
        'score': 0,
        'total': len(qdata),
        'game_type': 'blitz',
        'grade': 0,
        'answered': False,
    }
    _send_quiz_question(query, context)


# ══ КЕЙІПКЕРЛЕР ═══════════════════════════════════════════════════════════════════
def _start_character_game(query, context):
    questions = get_character_quizzes(8)
    qdata = []
    for q in questions:
        opts = q['opts'].copy()
        random.shuffle(opts)
        qdata.append({'q': q['q'], 'a': q['a'], 'opts': opts})
    context.user_data['quiz'] = {
        'questions': qdata,
        'current': 0,
        'score': 0,
        'total': len(qdata),
        'game_type': 'character',
        'grade': 0,
        'answered': False,
    }
    _send_quiz_question(query, context)
