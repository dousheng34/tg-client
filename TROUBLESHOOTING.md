# 🔧 ҚАТЕЛІКТЕРДІ ТҮЗЕТУ НҰСҚАУЛЫҒЫ

## 🚨 ЖИІ КЕЗДЕСЕТІН ҚАТЕЛІКТЕР

---

## 1️⃣ ОРНАТУ ҚАТЕЛІКТЕРІ

### Қате: ModuleNotFoundError: No module named 'telegram'

**Себебі:** python-telegram-bot модулі орнатылмаған

**Түзету:**
```bash
# Барлық модульдерді орнату
pip install -r requirements.txt

# Немесе тек telegram модулін орнату
pip install python-telegram-bot==20.7
```

**Тексеру:**
```bash
python -c "import telegram; print(telegram.__version__)"
# Нәтиже: 20.7
```

---

### Қате: Python version error

**Себебі:** Python 3.7-ден төмен версия

**Түзету:**
```bash
# Python версиясын тексеру
python --version

# Python 3.7+ орнату
# macOS
brew install python@3.9

# Ubuntu/Debian
sudo apt-get install python3.9

# Windows
# https://www.python.org/downloads/
```

---

### Қате: pip not found

**Себебі:** pip орнатылмаған

**Түзету:**
```bash
# pip орнату
python -m ensurepip --upgrade

# Немесе
sudo apt-get install python3-pip
```

---

## 2️⃣ ТОКЕН ҚАТЕЛІКТЕРІ

### Қате: Invalid token

**Себебі:** Токен дұрыс емес немесе орнатылмаған

**Түзету:**
```bash
# 1. @BotFather-ге Telegram-да жазыңыз
# 2. /start командасын жіберіңіз
# 3. /newbot командасын жіберіңіз
# 4. Бот атын енгізіңіз
# 5. Бот пайдаланушы атын енгізіңіз
# 6. Токенді көшіріңіз

# 2. kazakh_literature_bot.py файлын ашыңыз
# 3. TOKEN = "YOUR_BOT_TOKEN_HERE" жолын табыңыз
# 4. Өзгертіңіз: TOKEN = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"
```

**Тексеру:**
```bash
# Токенді тексеру
curl https://api.telegram.org/bot1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ/getMe
# Нәтиже: {"ok":true,"result":{"id":...}}
```

---

### Қате: Unauthorized

**Себебі:** Токен дұрыс емес

**Түзету:**
```bash
# Токенді қайта алыңыз
# @BotFather → /start → /mybots → Өзінің ботын таңдаңыз → API Token
```

---

## 3️⃣ БАЙЛАНЫС ҚАТЕЛІКТЕРІ

### Қате: Connection error / Network error

**Себебі:** Интернет байланысы жоқ немесе Telegram API қол жетімсіз

**Түзету:**
```bash
# 1. Интернет байланысын тексеру
ping google.com

# 2. Telegram API-ын тексеру
curl https://api.telegram.org/bot/getMe

# 3. Ботты қайта іске қосу
python kazakh_literature_bot.py

# 4. VPN пайдалану (егер Telegram блокталса)
```

---

### Қате: Timeout error

**Себебі:** Telegram API-ға жауап беру ұзақ уақыт алады

**Түзету:**
```python
# kazakh_literature_bot.py файлында
# Timeout-ты өзгертіңіз:

# Ағымдағы:
# request_kwargs={'read_timeout': 10}

# Жаңа:
# request_kwargs={'read_timeout': 30, 'connect_timeout': 30}
```

---

## 4️⃣ БОТТЫ ІСКЕ ҚОСУ ҚАТЕЛІКТЕРІ

### Қате: Бот іске қосылмайды

**Себебі:** Қандай да бір қате кодында

**Түзету:**
```bash
# 1. Логтарды оқыңыз
python kazakh_literature_bot.py 2>&1 | tee bot.log

# 2. Қателік мәтінін іздеңіз
grep -i "error" bot.log

# 3. Қателік мәтінін Google-та іздеңіз
# 4. Қателік мәтінін GitHub Issues-та іздеңіз
```

---

### Қате: Бот іске қосылды, бірақ командалар жұмыс істемейді

**Себебі:** Бот Telegram-та тіркелмеген

**Түзету:**
```bash
# 1. @BotFather-ге жазыңыз
# 2. /start командасын жіберіңіз
# 3. /mybots командасын жіберіңіз
# 4. Өзінің ботын таңдаңыз
# 5. Edit Commands басыңыз
# 6. Мына командаларды енгізіңіз:

start - Ботты іске қосу
авторлар - Авторлар тізімі
шығармалар - Шығармалар тізімі
кейіпкерлер - Кейіпкерлер тізімі
деректер - Қызықты деректер
ойын - Викторина бастау
ұпайлар - Ұпайларды көру
көмек - Барлық командалар
```

---

## 5️⃣ ОБЛАҚТА РАЗВЕРТЫВАНИЕ ҚАТЕЛІКТЕРІ

### Қате: Deployment failed

**Себебі:** requirements.txt файлы табылмады немесе модульдер орнатылмады

**Түзету:**
```bash
# 1. requirements.txt файлы болғанын тексеріңіз
ls -la requirements.txt

# 2. requirements.txt файлын жасаңыз
pip freeze > requirements.txt

# 3. GitHub-та сақтаңыз
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

---

### Қате: Build failed

**Себебі:** Python версиясы сәйкес емес

**Түзету:**
```bash
# 1. Koyeb/Render дашбордында Python версиясын өзгертіңіз
# 2. runtime.txt файлын жасаңыз
echo "python-3.9.18" > runtime.txt

# 3. GitHub-та сақтаңыз
git add runtime.txt
git commit -m "Add runtime.txt"
git push
```

---

### Қате: Application crashed

**Себебі:** Орта айнымалысы орнатылмаған

**Түзету:**
```bash
# 1. Облақ платформасының дашбордына барыңыз
# 2. Environment variables бөліміне барыңыз
# 3. BOT_TOKEN = YOUR_BOT_TOKEN_HERE орнатыңыз
# 4. Приложемені қайта іске қосыңыз
```

---

### Қате: Logs бөлімінде қателік көрсетіледі

**Түзету:**
```bash
# 1. Логтарды оқыңыз
# 2. Қателік мәтінін іздеңіз
# 3. Қателік мәтінін Google-та іздеңіз
# 4. Қателік мәтінін GitHub Issues-та іздеңіз
# 5. Қателік мәтінін Stack Overflow-та іздеңіз
```

---

## 6️⃣ ОЙЫНДАР ҚАТЕЛІКТЕРІ

### Қате: Викторина сұрағы көрсетілмейді

**Себебі:** QUIZ_QUESTIONS тізімі бос

**Түзету:**
```python
# kazakh_literature_bot.py файлында
# QUIZ_QUESTIONS тізімін тексеріңіз
# Сұрақтар болғанын тексеріңіз

print(len(QUIZ_QUESTIONS))  # Нәтиже: 8+
```

---

### Қате: Ұпайлар сақталмайды

**Себебі:** user_scores сөздігі сессия аяқталғанда өшіп кетеді

**Түзету:**
```python
# Деректер базасын пайдалану
# PostgreSQL немесе MongoDB-ге ауысыңыз
```

---

### Қате: Жауап нұсқалары көрсетілмейді

**Себебі:** Inline keyboard жасалмады

**Түзету:**
```python
# kazakh_literature_bot.py файлында
# send_quiz_question функциясын тексеріңіз
# Inline keyboard болғанын тексеріңіз
```

---

## 7️⃣ ІЗДЕУ ФУНКЦИЯСЫ ҚАТЕЛІКТЕРІ

### Қате: Іздеу нәтижесі көрсетілмейді

**Себебі:** Мазмұн базасында табылмады

**Түзету:**
```python
# kazakh_literature_bot.py файлында
# search_content функциясын тексеріңіз
# AUTHORS, WORKS, CHARACTERS сөздіктерін тексеріңіз
```

---

### Қате: Іздеу әрқашан "табылмады" хабарламасын көрсетеді

**Себебі:** Іздеу функциясы дұрыс емес

**Түзету:**
```python
# kazakh_literature_bot.py файлында
# search_content функциясын қайта жазыңыз

def search_content(query):
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

---

## 8️⃣ МӘЗІР ҚАТЕЛІКТЕРІ

### Қате: Мәзір түймелері көрсетілмейді

**Себебі:** Inline keyboard жасалмады

**Түзету:**
```python
# kazakh_literature_bot.py файлында
# start функциясын тексеріңіз
# Inline keyboard болғанын тексеріңіз
```

---

### Қате: Мәзір түймелері жұмыс істемейді

**Себебі:** Callback handler тіркелмеген

**Түзету:**
```python
# kazakh_literature_bot.py файлында
# Callback handler-ді тіркеңіз

dispatcher.add_handler(CallbackQueryHandler(button_callback))
```

---

## 9️⃣ ДЕРЕКТЕР БАЗАСЫ ҚАТЕЛІКТЕРІ

### Қате: Деректер сақталмайды

**Себебі:** Ағымдағы деректер базасы сессия аяқталғанда өшіп кетеді

**Түзету:**
```python
# PostgreSQL немесе MongoDB-ге ауысыңыз

# PostgreSQL орнату
pip install psycopg2-binary

# MongoDB орнату
pip install pymongo
```

---

### Қате: Деректер базасына қосылу қатесі

**Себебі:** Деректер базасы іске қосылмаған

**Түзету:**
```bash
# PostgreSQL іске қосу
sudo service postgresql start

# MongoDB іске қосу
sudo service mongod start
```

---

## 🔟 ОБЛАҚТА МОНИТОРИНГ ҚАТЕЛІКТЕРІ

### Қате: Бот ұйықтап қалды

**Себебі:** Облақ платформасы приложемені ұйықтатты

**Түзету:**
```bash
# 1. Облақ платформасының дашбордына барыңыз
# 2. Приложемені қайта іске қосыңыз
# 3. Health check орнатыңыз

# Koyeb-та:
# Health Check URL: /health
# Interval: 60 seconds

# Render-та:
# Health Check Path: /health
# Interval: 60 seconds
```

---

### Қате: Бот ағымдарының саны көбейді

**Себебі:** Бот ағымдарын жабу ұмытылды

**Түзету:**
```python
# kazakh_literature_bot.py файлында
# Ағымдарды жабу кодын қосыңыз

def main():
    try:
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        updater.stop()
        print("Бот тоқтатылды")
```

---

## 📋 ҚАТЕЛІКТЕРДІ ТҮЗЕТУ ЧЕК-ЛИСТІ

### Орнату
- [ ] Python 3.7+ орнатылған
- [ ] pip орнатылған
- [ ] requirements.txt орнатылған
- [ ] Модульдер орнатылған

### Токен
- [ ] Токен алынған
- [ ] Токен дұрыс орнатылған
- [ ] Токен тексерілген

### Байланыс
- [ ] Интернет байланысы бар
- [ ] Telegram API қол жетімді
- [ ] VPN қажет болса орнатылған

### Ботты іске қосу
- [ ] Бот іске қосылды
- [ ] Командалар жұмыс істейді
- [ ] Мәзір түймелері жұмыс істейді

### Облақта
- [ ] GitHub репозиториясы жасалған
- [ ] Облақ платформасы таңдалған
- [ ] Приложение жасалған
- [ ] Орта айнымалылары орнатылған
- [ ] Развертывание аяқталған
- [ ] Бот жұмыс істейді

---

## 📞 ҚОСЫМША КӨМЕК

### Ресурстар
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python-telegram-bot)
- [GitHub Issues](https://github.com/python-telegram-bot/python-telegram-bot/issues)

### Сұрақ бер
1. Логтарды оқы
2. Қателік мәтінін Google-та ізде
3. GitHub Issues-та ізде
4. Stack Overflow-та ізде
5. Telegram Bot API документациясын оқы

---

**Версия:** 4.0  
**Дата:** 8 апреля 2026 г.  
**Язык:** 100% Қазақша  
**Статус:** ✅ Толық дайын

