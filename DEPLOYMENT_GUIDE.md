# Telegram Bot Deployment Guide

## Часть 1: Локальное тестирование

### Шаг 1: Получить токен бота
1. Откройте Telegram и найдите @BotFather
2. Отправьте команду /newbot
3. Следуйте инструкциям:
   - Введите имя бота (например: KazLitEncyclopedia)
   - Введите username (например: kazlit_edu_bot)
4. Скопируйте полученный токен

### Шаг 2: Установить токен
Отредактируйте файл bot.py:
Замените TOKEN = "YOUR_BOT_TOKEN_HERE" на ваш токен

### Шаг 3: Запустить локально
```
source venv/bin/activate
python bot.py
```

---

## Часть 2: Развертывание на VPS (24/7)

### ВАРИАНТ 1: Render.com (РЕКОМЕНДУЕТСЯ) - Бесплатно или $7/месяц

Шаги:
1. Создайте GitHub репозиторий и загрузите код
2. Перейдите на render.com
3. Нажмите "New +" → "Web Service"
4. Подключите GitHub репозиторий
5. Заполните:
   - Name: telegram-bot
   - Runtime: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: python bot.py
6. Добавьте переменную окружения BOT_TOKEN
7. Нажмите Deploy

### ВАРИАНТ 2: DigitalOcean ($5/месяц) - ЛУЧШИЙ ВЫБОР

Шаги:
1. Создайте Droplet (Ubuntu 22.04, $5/месяц)
2. Подключитесь: ssh root@YOUR_SERVER_IP
3. Установите зависимости:
   apt update && apt upgrade -y
   apt install -y python3 python3-pip python3-venv git

4. Клонируйте репозиторий:
   cd /home
   git clone https://github.com/YOUR_USERNAME/telegram-bot.git
   cd telegram-bot

5. Создайте виртуальное окружение:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

6. Создайте systemd сервис для автозапуска
7. Запустите: sudo systemctl start telegram-bot

### ВАРИАНТ 3: AWS/Google Cloud (Бесплатно)

AWS EC2 (t2.micro) - бесплатно 12 месяцев
Google Cloud Run - бесплатно до 2 млн запросов/месяц

---

## Сравнение вариантов

Render.com: Бесплатно/$7 - Самый простой для начинающих
DigitalOcean: $5/месяц - Лучший выбор для надежности
AWS: Бесплатно 12 мес - Для опытных
Google Cloud: Бесплатно - Для опытных

---

## Полезные команды

Проверить статус бота (DigitalOcean):
sudo systemctl status telegram-bot

Просмотреть логи:
sudo journalctl -u telegram-bot -f

Перезагрузить бота:
sudo systemctl restart telegram-bot

Обновить код:
cd /home/telegram-bot
git pull origin main
sudo systemctl restart telegram-bot

---

## Решение проблем

Бот не отвечает:
1. Проверьте токен в bot.py
2. Проверьте интернет соединение
3. Посмотрите логи

Ошибка ModuleNotFoundError:
source venv/bin/activate
pip install -r requirements.txt

Бот падает после перезагрузки:
sudo systemctl enable telegram-bot

