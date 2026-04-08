# ⚡ ҚЫСҚА ОРНАТУ НҰСҚАУЛЫҒЫ

## 🚀 5 МИНУТТА ІСКЕ ҚОСУ

### Қадам 1: Токен алу (2 минут)
```
1. Telegram-да @BotFather ботына жазыңыз
2. /newbot командасын жіберіңіз
3. Бот атын енгізіңіз: KazLitEncyclopedia
4. Username енгізіңіз: kazlit_edu_bot
5. Токенді көшіріңіз (мысалы: 1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ)
```

### Қадам 2: Файлды өзгерту (1 минут)
```bash
# kazakh_literature_bot.py файлын ашыңыз
# Мына жолды табыңыз:
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Өзгертіңіз:
TOKEN = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"

# Сохраняйте файл (Ctrl+S)
```

### Қадам 3: Орнату (1 минут)
```bash
# Терминалды ашыңыз
cd /path/to/project

# Виртуалды орта жасаңыз
python3 -m venv venv

# Активтеу
source venv/bin/activate  # Mac/Linux
# немесе
venv\Scripts\activate     # Windows

# Кітапханаларды орнатыңыз
pip install -r requirements.txt
```

### Қадам 4: Іске қосу (1 минут)
```bash
python kazakh_literature_bot.py
```

✅ **Дайын!** Telegram-да ботыңызды іздеңіз және `/start` командасын жіберіңіз!

---

## 📱 ТЕСТ ЕТУ

Telegram-да ботыңызға мына командаларды жіберіңіз:

```
/start              → Мәзірді көрсету
/авторлар          → Авторлар тізімі
/шығармалар        → Шығармалар тізімі
/кейіпкерлер       → Кейіпкерлер тізімі
/деректер          → Қызықты деректер
/ойын              → Викторина бастау
/ұпайлар           → Ұпайларыңды көру
/көмек             → Барлық командалар
```

---

## 🐛 ҚАТЕЛІКТЕРДІ ТҮЗЕТУ

### Қате: "ModuleNotFoundError: No module named 'telegram'"
```bash
pip install -r requirements.txt
```

### Қате: "Invalid token"
- Токенді тексеріңіз
- @BotFather-ден жаңа токен алыңыз

### Қате: "Connection refused"
- Интернет байланысын тексеріңіз
- Ботты қайта іске қосыңыз

---

## 🌐 ОБЛАҚТА РАЗВЕРНУТЬ

### Koyeb (Ұсынылады)
1. https://www.koyeb.com сайтына барыңыз
2. GitHub репозиторийіңізді байланыстырыңыз
3. `kazakh_literature_bot.py` файлын таңдаңыз
4. Орта айнымалысын орнатыңыз: `BOT_TOKEN=ваш_токен`

### Render
1. https://render.com сайтына барыңыз
2. GitHub репозиторийіңізді байланыстырыңыз
3. Web Service құрыңыз
4. Орта айнымалысын орнатыңыз: `BOT_TOKEN=ваш_токен`

---

## ✅ ДАЙЫН!

Сіз барлығын орнаттыңыз! Енді ботты пайдалана аласыз! 🎉

