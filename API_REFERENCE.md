# 📚 API АНЫҚТАМАСЫ

## 🎯 БОТТЫ ПАЙДАЛАНУ

### Telegram Bot API

Бот python-telegram-bot 20.7 кітапханасын пайдаланады.

**Құрылымы:**
```
Telegram Bot API
    ↓
python-telegram-bot
    ↓
kazakh_literature_bot.py
    ↓
Пайдаланушы
```

---

## 📱 КОМАНДАЛАР API

### /start
**Сипаттамасы:** Ботты іске қосу

**Функция:**
```python
def start(update, context):
    """Ботты іске қосу"""
    user = update.effective_user
    message = f"🎓 Қош келдіңіз, {user.first_name}!\n\n"
    message += "Мен — Қазақ әдебиеті бот.\n"
    message += "Авторлар, шығармалар, кейіпкерлер туралы білу үшін командаларды пайдалан.\n\n"
    message += "📚 Авторлар\n"
    message += "📖 Шығармалар\n"
    message += "🎭 Кейіпкерлер\n"
    message += "💡 Қызықты деректер\n"
    message += "🎮 Викторина\n"
    message += "📊 Ұпайлар\n"
    message += "❓ Көмек\n"
    
    update.message.reply_text(message, reply_markup=get_main_menu())
```

**Параметрлер:**
- `update` — Telegram update объекты
- `context` — Контекст объекты

**Нәтиже:**
- Қош келдіңіз хабарламасы
- Мәзір түймелері

---

### /авторлар
**Сипаттамасы:** Авторлар тізімі

**Функция:**
```python
def authors(update, context):
    """Авторлар тізімін көрсету"""
    message = "📚 ҚАЗАҚ ӘДЕБИЕТІНІҢ АВТОРЛАРЫ\n"
    message += "═══════════════════════════════════════════════════════════════\n\n"
    
    for author_id, author in AUTHORS.items():
        message += f"📖 {author['name']}\n"
        message += f"📅 {author['years']}\n"
        message += f"🏠 {author['born']}\n"
        message += f"✍️ {author['style']}\n"
        message += f"📝 {author['bio']}\n"
        message += f"📚 Шығармалары: {', '.join(author['works_other'])}\n"
        message += "───────────────────────────────────────────────────────────────\n\n"
    
    update.message.reply_text(message)
```

**Параметрлер:**
- `update` — Telegram update объекты
- `context` — Контекст объекты

**Нәтиже:**
- Авторлар тізімі

---

### /шығармалар
**Сипаттамасы:** Шығармалар тізімі

**Функция:**
```python
def works(update, context):
    """Шығармалар тізімін көрсету"""
    message = "📖 ҚАЗАҚ ӘДЕБИЕТІНІҢ ШЫҒАРМАЛАРЫ\n"
    message += "═══════════════════════════════════════════════════════════════\n\n"
    
    for work_id, work in WORKS.items():
        message += f"📚 {work['title']}\n"
        message += f"✍️ {work['author']}\n"
        message += f"📅 {work['year']}\n"
        message += f"🎭 {work['genre']}\n"
        message += f"📝 {work['summary']}\n"
        message += f"💡 {work['idea']}\n"
        message += "───────────────────────────────────────────────────────────────\n\n"
    
    update.message.reply_text(message)
```

**Параметрлер:**
- `update` — Telegram update объекты
- `context` — Контекст объекты

**Нәтиже:**
- Шығармалар тізімі

---

### /кейіпкерлер
**Сипаттамасы:** Кейіпкерлер тізімі

**Функция:**
```python
def characters(update, context):
    """Кейіпкерлер тізімін көрсету"""
    message = "🎭 ҚАЗАҚ ӘДЕБИЕТІНІҢ КЕЙІПКЕРЛЕРІ\n"
    message += "═══════════════════════════════════════════════════════════════\n\n"
    
    for char_id, char in CHARACTERS.items():
        message += f"🎭 {char['name']}\n"
        message += f"📚 {char['work']}\n"
        message += f"📝 {char['description']}\n"
        message += f"✨ {char['traits']}\n"
        message += "───────────────────────────────────────────────────────────────\n\n"
    
    update.message.reply_text(message)
```

**Параметрлер:**
- `update` — Telegram update объекты
- `context` — Контекст объекты

**Нәтиже:**
- Кейіпкерлер тізімі

---

### /деректер
**Сипаттамасы:** Қызықты деректер

**Функция:**
```python
def facts(update, context):
    """Қызықты деректерді көрсету"""
    message = "💡 ҚЫЗЫҚТЫ ДЕРЕКТЕР\n"
    message += "═══════════════════════════════════════════════════════════════\n\n"
    
    for i, fact in enumerate(FACTS, 1):
        message += f"{i}. {fact}\n\n"
    
    update.message.reply_text(message)
```

**Параметрлер:**
- `update` — Telegram update объекты
- `context` — Контекст объекты

**Нәтиже:**
- Қызықты деректер тізімі

---

### /ойын
**Сипаттамасы:** Викторина бастау

**Функция:**
```python
def quiz(update, context):
    """Викторина сұрағын көрсету"""
    user_id = update.effective_user.id
    
    # Кездейсоқ сұрақ таңдау
    question = random.choice(QUIZ_QUESTIONS)
    
    # Сұрақ номерін сақтау
    context.user_data['current_question'] = question
    context.user_data['question_count'] = context.user_data.get('question_count', 0) + 1
    
    # Сұрақты көрсету
    message = f"🎮 ВИКТОРИНА #{context.user_data['question_count']}\n"
    message += "═══════════════════════════════════════════════════════════════\n\n"
    message += f"❓ {question['question']}\n\n"
    message += "Жауапты таңда:\n"
    
    # Inline keyboard жасау
    keyboard = [
        [InlineKeyboardButton("A) " + question['options'][0], callback_data=f"answer_0")],
        [InlineKeyboardButton("B) " + question['options'][1], callback_data=f"answer_1")],
        [InlineKeyboardButton("C) " + question['options'][2], callback_data=f"answer_2")],
        [InlineKeyboardButton("D) " + question['options'][3], callback_data=f"answer_3")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)
```

**Параметрлер:**
- `update` — Telegram update объекты
- `context` — Контекст объекты

**Нәтиже:**
- Викторина сұрағы
- Inline keyboard түймелері

---

### /ұпайлар
**Сипаттамасы:** Ұпайларды көру

**Функция:**
```python
def scores(update, context):
    """Ұпайларды көрсету"""
    user_id = update.effective_user.id
    
    total_score = user_scores.get(user_id, 0)
    correct_answers = correct_count.get(user_id, 0)
    total_questions = question_count.get(user_id, 0)
    
    percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    message = "📊 СЕНІҢ ҰПАЙЛАРЫҢ\n"
    message += "═══════════════════════════════════════════════════════════════\n\n"
    message += f"💰 Барлық ұпайлар: {total_score}\n"
    message += f"✅ Дұрыс жауаптар: {correct_answers}/{total_questions}\n"
    message += f"📈 Процент: {percentage:.1f}%\n\n"
    
    # Рейтинг беру
    if percentage >= 80:
        message += "🏆 Тамаша! Сен — шынайы білгір!\n"
    elif percentage >= 40:
        message += "👏 Жақсы нәтиже!\n"
    else:
        message += "📚 Оқуды жалғастыр!\n"
    
    update.message.reply_text(message)
```

**Параметрлер:**
- `update` — Telegram update объекты
- `context` — Контекст объекты

**Нәтиже:**
- Ұпайлар статистикасы
- Рейтинг

---

### /көмек
**Сипаттамасы:** Барлық командалар

**Функция:**
```python
def help_command(update, context):
    """Көмек хабарламасын көрсету"""
    message = "❓ КОМАНДАЛАР ТІЗІМІ\n"
    message += "═══════════════════════════════════════════════════════════════\n\n"
    message += "/start - Ботты іске қосу\n"
    message += "/авторлар - Авторлар тізімі\n"
    message += "/шығармалар - Шығармалар тізімі\n"
    message += "/кейіпкерлер - Кейіпкерлер тізімі\n"
    message += "/деректер - Қызықты деректер\n"
    message += "/ойын - Викторина бастау\n"
    message += "/ұпайлар - Ұпайларды көру\n"
    message += "/көмек - Барлық командалар\n\n"
    message += "💡 Авторлар, шығармалар немесе кейіпкерлер атын жаз, мен сізге ақпарат берем!\n"
    
    update.message.reply_text(message)
```

**Параметрлер:**
- `update` — Telegram update объекты
- `context` — Контекст объекты

**Нәтиже:**
- Командалар тізімі

---

## 🎮 CALLBACK HANDLERS

### answer_callback
**Сипаттамасы:** Викторина жауабын өңдеу

**Функция:**
```python
def answer_callback(update, context):
    """Викторина жауабын өңдеу"""
    query = update.callback_query
    user_id = query.from_user.id
    
    # Жауап нұсқасын алу
    answer_index = int(query.data.split('_')[1])
    
    # Ағымдағы сұрақты алу
    question = context.user_data.get('current_question')
    
    # Дұрыс жауапты тексеру
    if answer_index == question['correct']:
        query.answer_text("✅ Дұрыс жауап!")
        user_scores[user_id] = user_scores.get(user_id, 0) + 10
        correct_count[user_id] = correct_count.get(user_id, 0) + 1
        
        message = "✅ ДҰРЫС ЖАУАП!\n"
        message += "+10 ұпай 🎉\n\n"
        message += f"Сенің ұпайлары: {user_scores[user_id]}\n"
        message += f"Дұрыс жауаптар: {correct_count[user_id]}/{question_count[user_id]}\n"
    else:
        query.answer_text("❌ Қате жауап!")
        
        message = "❌ ҚАТЕ ЖАУАП!\n"
        message += f"Дұрыс жауап: {chr(65 + question['correct'])}) {question['options'][question['correct']]}\n\n"
        message += f"Сенің ұпайлары: {user_scores[user_id]}\n"
        message += f"Дұрыс жауаптар: {correct_count[user_id]}/{question_count[user_id]}\n"
    
    query.edit_message_text(text=message)
```

**Параметрлер:**
- `update` — Telegram update объекты
- `context` — Контекст объекты

**Нәтиже:**
- Жауап нәтижесі
- Ұпайлар жаңартылады

---

## 🔍 ІЗДЕУ ФУНКЦИЯСЫ

### search_content
**Сипаттамасы:** Авторлар, шығармалар, кейіпкерлерді іздеу

**Функция:**
```python
def search_content(query):
    """Мазмұнды іздеу"""
    query = query.lower()
    
    # Авторларды іздеу
    for author_id, author in AUTHORS.items():
        if query in author['name'].lower():
            return f"📖 {author['name']}\n{author['bio']}"
    
    # Шығармаларды іздеу
    for work_id, work in WORKS.items():
        if query in work['title'].lower():
            return f"📚 {work['title']}\n{work['summary']}"
    
    # Кейіпкерлерді іздеу
    for char_id, char in CHARACTERS.items():
        if query in char['name'].lower():
            return f"🎭 {char['name']}\n{char['description']}"
    
    return "🤔 Мен бұл туралы мазмұн базамда таба алмадым."
```

**Параметрлер:**
- `query` — Іздеу сұрағы

**Нәтиже:**
- Табылған мазмұн немесе "табылмады" хабарламасы

---

## 💾 ДЕРЕКТЕР ҚҰРЫЛЫМЫ

### AUTHORS
```python
AUTHORS = {
    "magzhan": {
        "name": "Мағжан Жұмабаев",
        "emoji": "📖",
        "years": "1893–1938",
        "born": "Түлкібас ауданы",
        "bio": "Өмірбаян...",
        "works_other": ["Батыр Баян", "Өлең жинағы"],
        "style": "Романтизм, символизм",
        "chapter": "balalar"
    }
}
```

### WORKS
```python
WORKS = {
    "batyr_bayan": {
        "title": "Батыр Баян",
        "author": "Мағжан Жұмабаев",
        "year": 1923,
        "genre": "Поэма",
        "summary": "Мазмұны...",
        "idea": "Идеясы...",
        "characters": ["Баян батыр"],
        "chapters": ["chapter1"]
    }
}
```

### CHARACTERS
```python
CHARACTERS = {
    "bayan": {
        "name": "Баян батыр",
        "work": "Батыр Баян",
        "description": "Сипаттамасы...",
        "traits": "Сипаттары..."
    }
}
```

### QUIZ_QUESTIONS
```python
QUIZ_QUESTIONS = [
    {
        "question": "«Батыр Баян» поэмасы қай жылы жазылды?",
        "options": ["1920", "1923", "1930", "1915"],
        "correct": 1,
        "author": "magzhan"
    }
]
```

---

## 🔐 ҚАУІПСІЗДІК

### Токен қорғау
```python
# ❌ ҚАТЕ
TOKEN = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"

# ✅ ДҰРЫС
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
```

### Орта айнымалылары
```bash
# .env файлы
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
```

---

## 📊 СТАТИСТИКА

| Метрика | Мәні |
|---------|------|
| Авторлар | 4 |
| Шығармалар | 4 |
| Кейіпкерлер | 6 |
| Викторина сұрақтары | 8+ |
| Қызықты деректер | 9+ |
| Командалар | 8 |

---

## 🚀 ОБЛАҚТА РАЗВЕРТЫВАНИЕ

### Орта айнымалылары
```
BOT_TOKEN = YOUR_BOT_TOKEN_HERE
```

### Health Check
```
GET /health
Response: {"status": "ok"}
```

---

**Версия:** 4.0  
**Дата:** 8 апреля 2026 г.  
**Язык:** 100% Қазақша  
**Статус:** ✅ Толық дайын

