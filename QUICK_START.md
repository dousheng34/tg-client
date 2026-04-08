# БЫСТРЫЙ СТАРТ - Telegram Bot

## 1️⃣ ЛОКАЛЬНОЕ ТЕСТИРОВАНИЕ (5 минут)

### Шаг 1: Получить токен
- Откройте Telegram → найдите @BotFather
- Отправьте /newbot
- Следуйте инструкциям, скопируйте токен

### Шаг 2: Установить токен в bot.py
Откройте bot.py и замените:
```
TOKEN = "YOUR_BOT_TOKEN_HERE"
```
На ваш токен:
```
TOKEN = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"
```

### Шаг 3: Запустить бота
```bash
source venv/bin/activate
python bot.py
```

Вы должны увидеть:
```
🚀 Бот іске қосылды! Ctrl+C басып тоқтатыңыз.
```

Откройте Telegram и найдите вашего бота по username!

---

## 2️⃣ РАЗВЕРТЫВАНИЕ НА СЕРВЕР (24/7)

### САМЫЙ ПРОСТОЙ СПОСОБ: Render.com (Бесплатно)

1. Создайте GitHub репозиторий и загрузите код:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot.git
git push -u origin main
```

2. Перейдите на https://render.com
3. Нажмите "New +" → "Web Service"
4. Подключите GitHub репозиторий
5. Заполните:
   - Name: telegram-bot
   - Runtime: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: python bot.py
6. Добавьте переменную окружения:
   - Key: BOT_TOKEN
   - Value: Ваш токен
7. Нажмите "Deploy"

Готово! Бот будет работать 24/7 бесплатно.

---

### БОЛЕЕ НАДЕЖНЫЙ СПОСОБ: DigitalOcean ($5/месяц)

1. Создайте Droplet на https://digitalocean.com
   - Image: Ubuntu 22.04
   - Size: $5/месяц
   - Получите IP адрес

2. Подключитесь к серверу:
```bash
ssh root@YOUR_SERVER_IP
```

3. Установите зависимости:
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv git
```

4. Клонируйте репозиторий:
```bash
cd /home
git clone https://github.com/YOUR_USERNAME/telegram-bot.git
cd telegram-bot
```

5. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. Создайте systemd сервис:
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Вставьте:
```
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

7. Запустите сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

8. Проверьте статус:
```bash
sudo systemctl status telegram-bot
```

Готово! Бот работает 24/7 на вашем сервере.

---

## 📊 СРАВНЕНИЕ

| Платформа | Стоимость | Простота | Надежность |
|-----------|-----------|----------|-----------|
| Render | Бесплатно | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| DigitalOcean | $5/месяц | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| AWS | Бесплатно (12 мес) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Рекомендация:** Начните с Render (бесплатно), потом перейдите на DigitalOcean для надежности.

---

## 🔧 ПОЛЕЗНЫЕ КОМАНДЫ

### Просмотреть логи (DigitalOcean)
```bash
sudo journalctl -u telegram-bot -f
```

### Перезагрузить бота
```bash
sudo systemctl restart telegram-bot
```

### Обновить код
```bash
cd /home/telegram-bot
git pull origin main
sudo systemctl restart telegram-bot
```

### Остановить бота
```bash
sudo systemctl stop telegram-bot
```

---

## ❓ РЕШЕНИЕ ПРОБЛЕМ

**Бот не отвечает:**
- Проверьте токен в bot.py
- Проверьте интернет соединение
- Посмотрите логи: `sudo journalctl -u telegram-bot -f`

**Ошибка "ModuleNotFoundError":**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Бот падает после перезагрузки сервера:**
```bash
sudo systemctl enable telegram-bot
```

---

## 📚 ДОПОЛНИТЕЛЬНЫЕ РЕСУРСЫ

- [python-telegram-bot документация](https://python-telegram-bot.readthedocs.io/)
- [Render.com документация](https://render.com/docs)
- [DigitalOcean документация](https://docs.digitalocean.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

