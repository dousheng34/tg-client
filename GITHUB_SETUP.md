# GitHub Setup для Telegram Bot

## Шаг 1: Создать репозиторий на GitHub

1. Перейдите на https://github.com/new
2. Заполните:
   - Repository name: `telegram-bot`
   - Description: `Telegram Bot - Kazakh Literature Encyclopedia`
   - Visibility: Public (для Render.com)
3. Нажмите "Create repository"

## Шаг 2: Инициализировать Git локально

```bash
cd /home/code
git init
git add .
git commit -m "Initial commit: Telegram bot setup"
```

## Шаг 3: Подключить к GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot.git
git branch -M main
git push -u origin main
```

Замените `YOUR_USERNAME` на ваше имя пользователя GitHub.

## Шаг 4: Проверить на GitHub

Откройте https://github.com/YOUR_USERNAME/telegram-bot

Вы должны увидеть все файлы:
- bot.py
- requirements.txt
- QUICK_START.md
- DEPLOYMENT_GUIDE.md
- Procfile
- .gitignore
- .env.example

## Готово!

Теперь вы можете развернуть бота на Render.com или DigitalOcean.

