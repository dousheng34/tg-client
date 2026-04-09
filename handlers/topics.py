"""
handlers/topics.py
Тақырыпқа кіру, оқу, сұрақ-жауап — толық handler
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from content.topics import get_topics, get_topic, get_topic_quiz, count_topics

import random


# ─── 1. Тақырыптар тізімі ───────────────────────────────────────────────────

def show_topics_list(update: Update, context: CallbackContext, grade: int):
    """Сынып бойынша тақырыптар тізімін көрсету"""
    query = update.callback_query
    query.answer()

    topics = get_topics(grade)
    if not topics:
        query.edit_message_text(
            f"❌ {grade}-сынып тақырыптары табылмады.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(f"◀️ {grade}-сынып", callback_data=f"enc_grade_{grade}")
            ]])
        )
        return

    keyboard = []
    for i, t in enumerate(topics):
        em = t.get("emoji", "📖")
        title = t.get("title", "Тақырып")
        # Ұзын тақырып атын қысқарту
        short_title = title[:30] + "..." if len(title) > 30 else title
        keyboard.append([
            InlineKeyboardButton(
                f"{em} {short_title}",
                callback_data=f"topic_read_{grade}_{t['id']}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("🧩 Жалпы тест", callback_data=f"topic_general_quiz_{grade}"),
        InlineKeyboardButton(f"◀️ {grade}-сынып", callback_data=f"enc_grade_{grade}")
    ])

    text = (
        f"<b>📚 {grade}-сынып тақырыптары</b>\n\n"
        f"📌 Барлығы: <b>{len(topics)} тақырып</b>\n"
        "═══════════════════════\n"
        "👇 Тақырыпты таңдаңыз:"
    )

    query.edit_message_text(
        text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── 2. Тақырыпты оқу ────────────────────────────────────────────────────────

def show_topic_content(update: Update, context: CallbackContext, grade: int, topic_id: str):
    """Тақырыптың толық мәтінін көрсету"""
    query = update.callback_query
    query.answer()

    topic = get_topic(grade, topic_id)
    if not topic:
        query.edit_message_text("❌ Тақырып табылмады.")
        return

    quiz_count = len(topic.get("quiz", []))

    keyboard = [
        [InlineKeyboardButton(
            f"🧩 Сұрақ-жауап ({quiz_count} сұрақ)",
            callback_data=f"topic_quiz_{grade}_{topic_id}_0"
        )],
        [
            InlineKeyboardButton("◀️ Тақырыптар", callback_data=f"topics_list_{grade}"),
            InlineKeyboardButton(f"◀️ {grade}-сынып", callback_data=f"enc_grade_{grade}")
        ]
    ]

    query.edit_message_text(
        topic["content"],
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── 3. Тақырып бойынша сұрақ-жауап ─────────────────────────────────────────

def show_topic_quiz(update: Update, context: CallbackContext,
                    grade: int, topic_id: str, q_index: int):
    """Тақырыптың сұрақ-жауаптарын кезекпен береді"""
    query = update.callback_query
    query.answer()

    quiz = get_topic_quiz(grade, topic_id)
    if not quiz:
        query.edit_message_text(
            "❌ Сұрақтар табылмады.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("◀️ Артқа", callback_data=f"topic_read_{grade}_{topic_id}")
            ]])
        )
        return

    if q_index >= len(quiz):
        # Тест аяқталды — нәтиже беру
        correct = context.user_data.get(f"topic_quiz_{grade}_{topic_id}_correct", 0)
        total = len(quiz)
        context.user_data.pop(f"topic_quiz_{grade}_{topic_id}_correct", None)

        if correct == total:
            result_emoji = "🏆"
            result_text = "Тамаша! Барлығы дұрыс!"
        elif correct >= total // 2:
            result_emoji = "✅"
            result_text = "Жақсы нәтиже!"
        else:
            result_emoji = "📖"
            result_text = "Тағы оқып, қайта тырыс!"

        topic = get_topic(grade, topic_id)
        text = (
            f"{result_emoji} <b>«{topic.get('title', '')}» тесті аяқталды</b>\n\n"
            f"✅ Дұрыс: <b>{correct}/{total}</b>\n"
            f"⭐ {result_text}\n\n"
        )

        keyboard = [
            [InlineKeyboardButton("🔄 Қайтадан", callback_data=f"topic_quiz_{grade}_{topic_id}_0")],
            [InlineKeyboardButton("📖 Тақырыпты оқу", callback_data=f"topic_read_{grade}_{topic_id}")],
            [InlineKeyboardButton("◀️ Тақырыптар", callback_data=f"topics_list_{grade}")]
        ]

        query.edit_message_text(text, parse_mode="HTML",
                                reply_markup=InlineKeyboardMarkup(keyboard))
        return

    q = quiz[q_index]
    options = q["opts"]

    # Жауап батырмалары
    keyboard = []
    for i, opt in enumerate(options):
        keyboard.append([
            InlineKeyboardButton(
                f"{'ABCД'[i]}. {opt}",
                callback_data=f"topic_answer_{grade}_{topic_id}_{q_index}_{i}"
            )
        ])
    keyboard.append([
        InlineKeyboardButton("◀️ Артқа", callback_data=f"topic_read_{grade}_{topic_id}")
    ])

    text = (
        f"🧩 <b>Сұрақ {q_index + 1}/{len(quiz)}</b>\n\n"
        f"❓ {q['q']}\n\n"
        "👇 Жауапты таңдаңыз:"
    )

    query.edit_message_text(text, parse_mode="HTML",
                            reply_markup=InlineKeyboardMarkup(keyboard))


# ─── 4. Жауапты тексеру ──────────────────────────────────────────────────────

def check_topic_answer(update: Update, context: CallbackContext,
                       grade: int, topic_id: str, q_index: int, chosen: int):
    """Жауапты тексеру және нәтиже беру"""
    query = update.callback_query
    query.answer()

    quiz = get_topic_quiz(grade, topic_id)
    if not quiz or q_index >= len(quiz):
        return

    q = quiz[q_index]
    correct_i = q["ai"]
    is_correct = (chosen == correct_i)

    # Дұрыс жауаптар санын сақта
    key = f"topic_quiz_{grade}_{topic_id}_correct"
    if is_correct:
        context.user_data[key] = context.user_data.get(key, 0) + 1

    # Жауап нәтижесі
    options = q["opts"]
    result_lines = []
    for i, opt in enumerate(options):
        if i == correct_i:
            result_lines.append(f"✅ {opt}")
        elif i == chosen and not is_correct:
            result_lines.append(f"❌ {opt}")
        else:
            result_lines.append(f"⬜ {opt}")

    result_emoji = "✅ Дұрыс!" if is_correct else "❌ Қате!"
    text = (
        f"🧩 <b>Сұрақ {q_index + 1}/{len(quiz)}</b>\n\n"
        f"❓ {q['q']}\n\n"
        "\n".join(result_lines) + "\n\n"
        f"<b>{result_emoji}</b>"
    )

    next_index = q_index + 1
    keyboard = [[
        InlineKeyboardButton(
            "➡️ Келесі сұрақ" if next_index < len(quiz) else "🏆 Нәтиже",
            callback_data=f"topic_quiz_{grade}_{topic_id}_{next_index}"
        )
    ]]

    query.edit_message_text(text, parse_mode="HTML",
                            reply_markup=InlineKeyboardMarkup(keyboard))


# ─── 5. Жалпы тест (барлық тақырыптардан) ───────────────────────────────────

def show_general_quiz(update: Update, context: CallbackContext, grade: int):
    """Сынып бойынша жалпы тест — барлық тақырыптардан 10 сұрақ"""
    query = update.callback_query
    query.answer()

    topics = get_topics(grade)
    all_quiz = []
    for t in topics:
        for q in t.get("quiz", []):
            all_quiz.append((t["id"], q))

    if not all_quiz:
        query.edit_message_text(
            "❌ Сұрақтар табылмады.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("◀️ Артқа", callback_data=f"topics_list_{grade}")
            ]])
        )
        return

    # 10 кездейсоқ сұрақ
    selected = random.sample(all_quiz, min(10, len(all_quiz)))
    context.user_data[f"general_quiz_{grade}"] = selected
    context.user_data[f"general_quiz_{grade}_score"] = 0

    # Бірінші сұрақты көрсет
    _show_general_question(query, context, grade, 0)


def _show_general_question(query, context: CallbackContext, grade: int, q_index: int):
    """Жалпы тесттің сұрақтарын беру"""
    selected = context.user_data.get(f"general_quiz_{grade}", [])

    if q_index >= len(selected):
        score = context.user_data.get(f"general_quiz_{grade}_score", 0)
        total = len(selected)
        context.user_data.pop(f"general_quiz_{grade}", None)
        context.user_data.pop(f"general_quiz_{grade}_score", None)

        if score == total:
            em = "🏆"
        elif score >= total // 2:
            em = "✅"
        else:
            em = "📖"

        text = (
            f"{em} <b>{grade}-сынып жалпы тест аяқталды!</b>\n\n"
            f"✅ Дұрыс жауап: <b>{score}/{total}</b>\n\n"
        )

        query.edit_message_text(
            text, parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Қайтадан", callback_data=f"topic_general_quiz_{grade}")],
                [InlineKeyboardButton("◀️ Тақырыптар", callback_data=f"topics_list_{grade}")]
            ])
        )
        return

    topic_id, q = selected[q_index]
    options = q["opts"]

    keyboard = []
    for i, opt in enumerate(options):
        keyboard.append([
            InlineKeyboardButton(
                f"{'ABCД'[i]}. {opt}",
                callback_data=f"general_answer_{grade}_{q_index}_{i}"
            )
        ])

    text = (
        f"🧩 <b>{grade}-сынып жалпы тест</b> | Сұрақ {q_index + 1}/{len(selected)}\n\n"
        f"❓ {q['q']}\n\n"
        "👇 Жауапты таңдаңыз:"
    )

    query.edit_message_text(text, parse_mode="HTML",
                            reply_markup=InlineKeyboardMarkup(keyboard))


def check_general_answer(update: Update, context: CallbackContext,
                         grade: int, q_index: int, chosen: int):
    """Жалпы тест жауабын тексеру"""
    query = update.callback_query
    query.answer()

    selected = context.user_data.get(f"general_quiz_{grade}", [])
    if not selected or q_index >= len(selected):
        return

    _, q = selected[q_index]
    correct_i = q["ai"]
    is_correct = (chosen == correct_i)

    if is_correct:
        context.user_data[f"general_quiz_{grade}_score"] = \
            context.user_data.get(f"general_quiz_{grade}_score", 0) + 1

    options = q["opts"]
    lines = []
    for i, opt in enumerate(options):
        if i == correct_i:
            lines.append(f"✅ {opt}")
        elif i == chosen and not is_correct:
            lines.append(f"❌ {opt}")
        else:
            lines.append(f"⬜ {opt}")

    text = (
        f"🧩 <b>Сұрақ {q_index + 1}/{len(selected)}</b>\n\n"
        f"❓ {q['q']}\n\n"
        "\n".join(lines) + "\n\n"
        f"<b>{'✅ Дұрыс!' if is_correct else '❌ Қате!'}</b>"
    )

    keyboard = [[
        InlineKeyboardButton(
            "➡️ Келесі" if q_index + 1 < len(selected) else "🏆 Нәтиже",
            callback_data=f"general_answer_{grade}_{q_index + 1}_show"
        )
    ]]

    query.edit_message_text(text, parse_mode="HTML",
                            reply_markup=InlineKeyboardMarkup(keyboard))


def show_next_general_question(update: Update, context: CallbackContext,
                               grade: int, q_index: int):
    """Жалпы тесттің келесі сұрағына өту"""
    query = update.callback_query
    query.answer()
    _show_general_question(query, context, grade, q_index)
