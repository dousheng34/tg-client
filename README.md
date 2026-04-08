# 🤖 Telegram Bot - Казахская Литература

Полнофункциональный Telegram бот для изучения казахской литературы (5-7 классы).

## 📋 Содержание

- [Быстрый старт](#быстрый-старт)
- [Локальное тестирование](#локальное-тестирование)
- [Развертывание на сервер](#развертывание-на-сервер)
- [Структура проекта](#структура-проекта)
- [Команды](#команды)

---

## 🚀 Быстрый старт

### Требования
- Python 3.8+
- pip
- Telegram аккаунт

### Шаг 1: Получить токен бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Следуйте инструкциям и скопируйте токен

### Шаг 2: Установить окружение

```bash
# Создать виртуальное окружение
python3 -m venv venv

# Активировать
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt
```

### Шаг 3: Установить токен

Откройте `bot.py` и замените:
```python
TOKEN = "YOUR_BOT_TOKEN_HERE"
```

На ваш токен:
```python
TOKEN = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"
```

### Шаг 4: Запустить бота

```bash
python bot.py
```

Вы должны увидеть:
```
🚀 Бот іске қосылды! Ctrl+C басып тоқтатыңыз.
```

Откройте Telegram и найдите вашего бота по username!

---

## 🧪 Локальное тестирование

### Функции бота

- 📚 **Сыныптар** - Информация о классах
- ✍️ **Авторлар** - Биография авторов
- 📖 **Шығармалар** - Описание произведений
- 🎭 **Кейіпкерлер** - Характеристика персонажей

### Тестирование

1. Отправьте `/start` боту
2. Нажимайте кнопки для навигации
3. Проверьте все разделы

---

## 🌐 Развертывание на сервер

### Вариант 1: Render.com (РЕКОМЕНДУЕТСЯ - Бесплатно)

**Простота:** ⭐⭐⭐⭐⭐  
**Стоимость:** Бесплатно

#### Шаги:

1. **Создать GitHub репозиторий:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot.git
git push -u origin main
```

2. **Развернуть на Render:**
   - Перейдите на [render.com](https://render.com)
   - Нажмите "New +" → "Web Service"
   - Подключите GitHub репозиторий
   - Заполните:
     - Name: `telegram-bot`
     - Runtime: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python bot.py`
   - Добавьте переменную окружения:
     - Key: `BOT_TOKEN`
     - Value: Ваш токен
   - Нажмите "Deploy"

3. **Готово!** Бот работает 24/7 бесплатно.

---

### Вариант 2: DigitalOcean ($5/месяц) - ЛУЧШИЙ ВЫБОР

**Простота:** ⭐⭐⭐⭐  
**Стоимость:** $5/месяц  
**Надежность:** ⭐⭐⭐⭐⭐

#### Шаги:

1. **Создать Droplet:**
   - Перейдите на [digitalocean.com](https://digitalocean.com)
   - Создайте новый Droplet:
     - Image: Ubuntu 22.04
     - Size: $5/месяц
   - Получите IP адрес

2. **Подключиться к серверу:**
```bash
ssh root@YOUR_SERVER_IP
```

3. **Установить зависимости:**
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv git
```

4. **Клонировать репозиторий:**
```bash
cd /home
git clone https://github.com/YOUR_USERNAME/telegram-bot.git
cd telegram-bot
```

5. **Создать виртуальное окружение:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Создать systemd сервис:**
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Вставьте:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/telegram-bot
Environment="PATH=/home/telegram-bot/venv/bin"
ExecStart=/home/telegram-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Сохраните (Ctrl+X, Y, Enter)

7. **Запустить сервис:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

8. **Проверить статус:**
```bash
sudo systemctl status telegram-bot
```

---

## 📁 Структура проекта

```
telegram-bot/
├── bot.py                    # Основной файл бота
├── requirements.txt          # Зависимости Python
├── Procfile                  # Для Render.com
├── .env.example              # Пример переменных окружения
├── .gitignore                # Для Git
├── venv/                     # Виртуальное окружение
├── README.md                 # Этот файл
├── QUICK_START.md            # Быстрый старт
├── DEPLOYMENT_GUIDE.md       # Полное руководство
├── GITHUB_SETUP.md           # Инструкция по GitHub
└── SETUP_SUMMARY.txt         # Итоговый summary
```

---

## 🔧 Команды

### Локальное тестирование

```bash
# Активировать виртуальное окружение
source venv/bin/activate

# Запустить бота
python bot.py

# Деактивировать окружение
deactivate
```

### DigitalOcean

```bash
# Просмотреть логи
sudo journalctl -u telegram-bot -f

# Перезагрузить бота
sudo systemctl restart telegram-bot

# Остановить бота
sudo systemctl stop telegram-bot

# Запустить бота
sudo systemctl start telegram-bot

# Проверить статус
sudo systemctl status telegram-bot
```

### Обновление кода

```bash
cd /home/telegram-bot
git pull origin main
sudo systemctl restart telegram-bot
```

---

## 📚 Дополнительные ресурсы

- [python-telegram-bot документация](https://python-telegram-bot.readthedocs.io/)
- [Render.com документация](https://render.com/docs)
- [DigitalOcean документация](https://docs.digitalocean.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## ❓ Решение проблем

### Бот не отвечает
- Проверьте токен в `bot.py`
- Проверьте интернет соединение
- Посмотрите логи: `sudo journalctl -u telegram-bot -f`

### Ошибка "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Бот падает после перезагрузки сервера
```bash
sudo systemctl enable telegram-bot
```

---

## 📝 Лицензия

MIT License

---

## 👨‍💻 Автор

Создано как учебный проект для изучения казахской литературы.

---

**Начните с [QUICK_START.md](QUICK_START.md) для быстрого старта!** 🚀

