# 🚀 ОБЛАҚТА РАЗВЕРТЫВАНИЕ НҰСҚАУЛЫҒЫ

## 📋 ҚАЖЕТТІ НӘРСЕЛЕР

- ✅ GitHub аккаунты
- ✅ Telegram бот токені (@BotFather-ден)
- ✅ Облақ платформасының аккаунты (Koyeb, Render, Heroku, т.б.)
- ✅ Git орнатылған

---

## 🔧 ҚАДАМ 1: GitHub-та репозиторий жасау

### 1.1 GitHub-та жаңа репозиторий жасау
```bash
1. https://github.com/new қарай барыңыз
2. Repository name: tg-kazakh-literature-bot
3. Description: Kazakh Literature Telegram Bot
4. Public немесе Private таңдаңыз
5. Create repository басыңыз
```

### 1.2 Локалды репозиторийді GitHub-та сақтау
```bash
cd /home/code

# Git инициализациялау
git init

# GitHub репозиториясын қосу
git remote add origin https://github.com/YOUR_USERNAME/tg-kazakh-literature-bot.git

# Барлық файлдарды қосу
git add .

# Коммит жасау
git commit -m "Initial commit: Kazakh Literature Bot v4.0"

# GitHub-та сақтау
git branch -M main
git push -u origin main
```

---

## 🌐 ҚАДАМ 2: Koyeb-та развертывание (ҰСЫНЫЛАДЫ)

### 2.1 Koyeb аккаунты жасау
```
1. https://www.koyeb.com қарай барыңыз
2. Sign up басыңыз
3. Email және пароль енгізіңіз
4. Аккаунтты растаңыз
```

### 2.2 Koyeb-та приложение жасау
```
1. Koyeb дашбордына кіріңіз
2. Create Service басыңыз
3. GitHub таңдаңыз
4. Өзінің репозиториясын таңдаңыз (tg-kazakh-literature-bot)
5. Branch: main
6. Builder: Buildpack
7. Run command: python kazakh_literature_bot.py
```

### 2.3 Орта айнымалыларын орнату
```
1. Environment variables бөліміне барыңыз
2. Жаңа айнымалы қосыңыз:
   - Name: BOT_TOKEN
   - Value: YOUR_BOT_TOKEN_HERE
3. Save басыңыз
```

### 2.4 Развертывание бастау
```
1. Deploy басыңыз
2. Орнату процесін күтіңіз (5-10 минут)
3. ✅ Deployment successful хабарламасын күтіңіз
```

**Koyeb URL:** https://your-app-name.koyeb.app

---

## 🎨 ҚАДАМ 3: Render-та развертывание (АЛЬТЕРНАТИВА)

### 3.1 Render аккаунты жасау
```
1. https://render.com қарай барыңыз
2. Sign up басыңыз
3. GitHub аккаунтын байланыстырыңыз
```

### 3.2 Render-та приложение жасау
```
1. Render дашбордына кіріңіз
2. New + → Web Service
3. GitHub репозиториясын таңдаңыз
4. Name: tg-kazakh-literature-bot
5. Environment: Python 3
6. Build command: pip install -r requirements.txt
7. Start command: python kazakh_literature_bot.py
```

### 3.3 Орта айнымалыларын орнату
```
1. Environment бөліміне барыңыз
2. BOT_TOKEN = YOUR_BOT_TOKEN_HERE
3. Save and Deploy басыңыз
```

---

## 🟣 ҚАДАМ 4: Heroku-та развертывание

### 4.1 Heroku аккаунты жасау
```
1. https://www.heroku.com қарай барыңыз
2. Sign up басыңыз
3. Email растаңыз
```

### 4.2 Heroku CLI орнату
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Windows
# https://devcenter.heroku.com/articles/heroku-cli#download-and-install
```

### 4.3 Heroku-та приложение жасау
```bash
# Heroku-та кіру
heroku login

# Приложение жасау
heroku create tg-kazakh-literature-bot

# Орта айнымалысын орнату
heroku config:set BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# GitHub-та сақтау
git push heroku main

# Логтарды көру
heroku logs --tail
```

---

## 🚂 ҚАДАМ 5: Railway-та развертывание

### 5.1 Railway аккаунты жасау
```
1. https://railway.app қарай барыңыз
2. Sign up басыңыз
3. GitHub аккаунтын байланыстырыңыз
```

### 5.2 Railway-та приложение жасау
```
1. Railway дашбордына кіріңіз
2. New Project → GitHub Repo
3. Өзінің репозиториясын таңдаңыз
4. Deploy басыңыз
```

### 5.3 Орта айнымалыларын орнату
```
1. Variables бөліміне барыңыз
2. BOT_TOKEN = YOUR_BOT_TOKEN_HERE
3. Save басыңыз
```

---

## 💻 ҚАДАМ 6: Replit-та развертывание

### 6.1 Replit аккаунты жасау
```
1. https://replit.com қарай барыңыз
2. Sign up басыңыз
3. GitHub аккаунтын байланыстырыңыз
```

### 6.2 Replit-та приложение жасау
```
1. Replit дашбордына кіріңіз
2. Import from GitHub
3. Өзінің репозиториясын таңдаңыз
4. Import басыңыз
```

### 6.3 Орта айнымалыларын орнату
```
1. Secrets (🔒) бөліміне барыңыз
2. BOT_TOKEN = YOUR_BOT_TOKEN_HERE
3. Run басыңыз
```

---

## ✅ ҚАДАМ 7: Развертывание тексеру

### 7.1 Бот жұмыс істейтінін тексеру
```bash
# Telegram-да ботыңызға мына командаларды жіберіңіз:
/start
/авторлар
/ойын
/ұпайлар
```

### 7.2 Логтарды көру
```bash
# Koyeb
# Koyeb дашбордында Logs бөліміне барыңыз

# Render
# Render дашбордында Logs бөліміне барыңыз

# Heroku
heroku logs --tail

# Railway
# Railway дашбордында Logs бөліміне барыңыз

# Replit
# Replit консолында логтарды көріңіз
```

### 7.3 Қателіктерді түзету
```bash
# Қате: ModuleNotFoundError
# Түзету: requirements.txt файлы болғанын тексеріңіз

# Қате: Invalid token
# Түзету: BOT_TOKEN дұрыс орнатылғанын тексеріңіз

# Қате: Connection error
# Түзету: Интернет байланысын тексеріңіз
```

---

## 🔄 ҚАДАМ 8: Автоматты обновление

### 8.1 GitHub Actions орнату (Koyeb, Render)
```yaml
# .github/workflows/deploy.yml файлын жасаңыз

name: Deploy to Koyeb

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Koyeb
      run: |
        # Koyeb API-ын пайдалану
        curl -X POST https://api.koyeb.com/v1/deployments \
          -H "Authorization: Bearer ${{ secrets.KOYEB_TOKEN }}" \
          -d '{"service": "tg-kazakh-literature-bot"}'
```

### 8.2 Webhook орнату
```
1. GitHub репозиториясына барыңыз
2. Settings → Webhooks
3. Add webhook
4. Payload URL: https://your-app.koyeb.app/webhook
5. Content type: application/json
6. Add webhook
```

---

## 📊 МОНИТОРИНГ

### 7.1 Бот статусын мониторинг қылу
```bash
# Koyeb
# Koyeb дашбордында Status бөліміне барыңыз

# Render
# Render дашбордында Health Check бөліміне барыңыз

# Heroku
heroku ps

# Railway
# Railway дашбордында Deployments бөліміне барыңыз
```

### 7.2 Қателіктерді мониторинг қылу
```bash
# Koyeb
# Logs бөліміне барыңыз және қателіктерді іздеңіз

# Render
# Logs бөліміне барыңіз және қателіктерді іздеңіз

# Heroku
heroku logs --tail --source app

# Railway
# Logs бөліміне барыңыз және қателіктерді іздеңіз
```

---

## 🔐 ҚАУІПСІЗДІК

### 8.1 Токенді қорғау
```
❌ ҚАТЕ: TOKEN = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"
✅ ДҰРЫС: Орта айнымалыларын пайдалану
```

### 8.2 Орта айнымалыларын пайдалану
```python
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
```

### 8.3 .env файлын .gitignore-та сақтау
```bash
# .gitignore файлын жасаңыз
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
git push
```

---

## 📈 МАСШТАБТАУ

### 9.1 Бот ағымдарын көбейту
```python
# kazakh_literature_bot.py файлында
# Бот ағымдарын көбейтіңіз:
# - Main polling thread
# - HTTP health check thread
# - Database update thread
```

### 9.2 Деректер базасын масштабтау
```python
# Ағымдағы деректер базасынан
# PostgreSQL немесе MongoDB-ге ауысыңыз
```

### 9.3 Облақ ресурстарын көбейту
```
1. Koyeb: Dyno type-ін өзгертіңіз
2. Render: Instance type-ін өзгертіңіз
3. Heroku: Dyno type-ін өзгертіңіз
4. Railway: CPU/RAM-ды өзгертіңіз
```

---

## 🎯 ФИНАЛДЫ ТЕКСЕРУ

### Чек-лист
- [ ] GitHub репозиториясы жасалған
- [ ] Облақ платформасы таңдалған
- [ ] Приложение жасалған
- [ ] Орта айнымалылары орнатылған
- [ ] Развертывание аяқталған
- [ ] Бот жұмыс істейді
- [ ] Логтарда қателік жоқ
- [ ] Командалар жұмыс істейді
- [ ] Ойындар жұмыс істейді
- [ ] Іздеу функциясы жұмыс істейді

---

## 📞 ҚОЛДАУ

### Қателіктерді түзету
1. Логтарды оқыңыз
2. Орта айнымалыларын тексеріңіз
3. Токенді тексеріңіз
4. Интернет байланысын тексеріңіз

### Қосымша ресурстар
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [Koyeb Docs](https://docs.koyeb.com/)
- [Render Docs](https://render.com/docs)
- [Heroku Docs](https://devcenter.heroku.com/)

---

**Версия:** 4.0  
**Дата:** 8 апреля 2026 г.  
**Язык:** 100% Қазақша  
**Статус:** ✅ Толық дайын

