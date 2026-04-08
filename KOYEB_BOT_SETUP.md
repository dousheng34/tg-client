# 🔧 Настройка bot.py для Koyeb

## Важно: Переменные окружения

Ваш `bot.py` должен читать токен из переменной окружения `TELEGRAM_BOT_TOKEN`, а не из `.env` файла.

---

## ✅ Правильная конфигурация для Koyeb

Убедитесь, что в начале `bot.py` у вас есть:

```python
import os
from dotenv import load_dotenv

# Загрузить переменные из .env (для локального тестирования)
load_dotenv()

# Получить токен из переменной окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Проверка, что токен установлен
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен!")
```

---

## 📝 Полный пример начала bot.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Загрузить переменные из .env (для локального тестирования)
load_dotenv()

# Получить токен из переменной окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Проверка, что токен установлен
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен! Проверьте переменные окружения.")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ... остальной код бота ...
```

---

## 🔄 Как это работает

### Локально (на вашем компьютере)

1. Создайте файл `.env`:
```
TELEGRAM_BOT_TOKEN=8167312154:AAFNFQqJ7_dwbbqFjlO4tTbpGSkD9lQP4rM
```

2. Запустите бота:
```bash
python bot.py
```

3. `python-dotenv` загрузит переменные из `.env`

### На Koyeb

1. Вы устанавливаете переменную окружения в Koyeb:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: `8167312154:AAFNFQqJ7_dwbbqFjlO4tTbpGSkD9lQP4rM`

2. Koyeb передает эту переменную вашему приложению

3. `os.getenv('TELEGRAM_BOT_TOKEN')` получает значение из переменной окружения

---

## ✨ Преимущества этого подхода

✅ **Безопасность** — токен не хранится в коде  
✅ **Гибкость** — работает локально и на сервере  
✅ **Простота** — одна строка кода для получения токена  
✅ **Стандарт** — это лучшая практика в индустрии  

---

## 🚀 Проверка перед развертыванием

Перед загрузкой на Koyeb убедитесь:

1. ✅ В `bot.py` есть `import os`
2. ✅ В `bot.py` есть `from dotenv import load_dotenv`
3. ✅ В `bot.py` есть `load_dotenv()`
4. ✅ Токен получается через `os.getenv('TELEGRAM_BOT_TOKEN')`
5. ✅ В `requirements.txt` есть `python-dotenv`
6. ✅ `.env` файл в `.gitignore` (не загружается на GitHub)

---

## 📋 Чеклист перед развертыванием на Koyeb

- [ ] `bot.py` использует `os.getenv('TELEGRAM_BOT_TOKEN')`
- [ ] `requirements.txt` содержит все зависимости
- [ ] `.env` файл в `.gitignore`
- [ ] Код загружен на GitHub
- [ ] Koyeb переменная окружения установлена правильно
- [ ] Локально бот работает с `.env` файлом

---

## 🐛 Если что-то не работает

### Ошибка: "TELEGRAM_BOT_TOKEN не установлен!"

**Решение:**
1. Проверьте, что переменная окружения установлена на Koyeb
2. Проверьте, что имя переменной точно `TELEGRAM_BOT_TOKEN`
3. Перезагрузите приложение на Koyeb
4. Посмотрите логи на Koyeb

### Ошибка: "ModuleNotFoundError: No module named 'dotenv'"

**Решение:**
1. Убедитесь, что `python-dotenv` в `requirements.txt`
2. Перезагрузите приложение на Koyeb

### Бот не отвечает

**Решение:**
1. Проверьте логи на Koyeb
2. Убедитесь, что приложение в статусе "Running"
3. Проверьте, что токен правильный
4. Перезагрузите приложение

---

## 📚 Дополнительные ресурсы

- [Документация python-dotenv](https://python-dotenv.readthedocs.io/)
- [Переменные окружения в Python](https://docs.python.org/3/library/os.html#os.getenv)
- [Документация Koyeb](https://docs.koyeb.com)

---

**Готово! Ваш бот готов к развертыванию на Koyeb! 🚀**
