# 📤 Инструкция: Загрузка проекта на GitHub

## Шаг 1: Создать репозиторий на GitHub

1. Перейдите на https://github.com/new
2. Заполните:
   - **Repository name:** `telegram-bot` (или другое имя)
   - **Description:** `Telegram Bot - Kazakh Literature Encyclopedia`
   - **Visibility:** Public (для Render.com) или Private (если нужно)
3. **НЕ** инициализируйте README, .gitignore или лицензию (они уже есть)
4. Нажмите "Create repository"

## Шаг 2: Получить команды для загрузки

После создания репозитория GitHub покажет вам команды. Они будут выглядеть так:

```bash
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot.git
git branch -M main
git push -u origin main
```

## Шаг 3: Выполнить команды в терминале

```bash
# Перейти в папку проекта
cd /home/code

# Добавить удаленный репозиторий
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot.git

# Переименовать ветку в main (если нужно)
git branch -M main

# Загрузить код на GitHub
git push -u origin main
```

**Замените `YOUR_USERNAME` на ваше имя пользователя GitHub!**

## Шаг 4: Проверить на GitHub

Откройте https://github.com/YOUR_USERNAME/telegram-bot

Вы должны увидеть все файлы:
- bot.py
- requirements.txt
- README.md
- QUICK_START.md
- DEPLOYMENT_GUIDE.md
- И другие файлы

## ✅ Готово!

Теперь вы можете:
1. Развернуть на Render.com (см. QUICK_START.md)
2. Развернуть на DigitalOcean (см. QUICK_START.md)
3. Делиться ссылкой на репозиторий с клиентом

---

## 🔑 Важные моменты

- **Токен бота НЕ загружайте на GitHub!** Используйте переменные окружения (BOT_TOKEN)
- Файл `.env.example` показывает, какие переменные нужны
- Файл `.gitignore` защищает от случайной загрузки чувствительных данных

---

## ❓ Если возникли проблемы

### Ошибка: "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot.git
```

### Ошибка: "Permission denied (publickey)"
Нужно настроить SSH ключи для GitHub:
https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Ошибка: "Updates were rejected"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## 📚 Дополнительные ресурсы

- [GitHub документация](https://docs.github.com/)
- [Git документация](https://git-scm.com/doc)
- [SSH ключи для GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

