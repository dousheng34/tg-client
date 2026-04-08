# 🚀 DEPLOYMENT ҚҰЖАТЫ
## Қазақ Әдебиеті Telegram Боты v4.0

---

## 📋 Мазмұны
1. [Қалыптастыру](#қалыптастыру)
2. [Koyeb-ке орнату](#koyeb-ке-орнату)
3. [Render-ге орнату](#render-ге-орнату)
4. [Docker-мен орнату](#docker-мен-орнату)
5. [Локалды тестілеу](#локалды-тестілеу)
6. [Мониторинг және логирование](#мониторинг-және-логирование)
7. [Қауіпсіздік](#қауіпсіздік)

---

## 🔧 Қалыптастыру

### Өндіктемелер
- Python 3.9+
- pip немесе poetry
- Git
- Docker (опционалды)

### Орнату қадамдары

```bash
# Репозиторийді клондау
git clone https://github.com/your-username/kazakh-literature-bot.git
cd kazakh-literature-bot

# Virtual environment жасау
python -m venv venv
source venv/bin/activate  # Linux/Mac
# немесе
venv\Scripts\activate  # Windows

# Зависимостілерді орнату
pip install -r requirements.txt

# .env файлын жасау
cp .env.example .env
# .env файлын өндіктеңіз және BOT_TOKEN-ді қосыңыз
```

### .env файлын конфигурациялау

```env
# Telegram Bot Token (https://t.me/BotFather)
BOT_TOKEN=your_bot_token_here

# Орта
ENVIRONMENT=development  # development | production

# Логирование
LOG_LEVEL=INFO
LOG_FILE=bot.log

# Веб-сервер
PORT=8000
HOST=0.0.0.0
```

---

## 🌐 Koyeb-ке орнату

### Қадам 1: GitHub репозиторийін дайындау

```bash
# GitHub-та жаңа репозиторий жасаңыз
git remote add origin https://github.com/your-username/kazakh-literature-bot.git
git branch -M main
git push -u origin main
```

### Қадам 2: Koyeb-те орнату

1. [Koyeb.com](https://www.koyeb.com) сайтына кіріңіз
2. **Create Service** батонын басыңыз
3. **GitHub** таңдаңыз
4. Репозиторийіңізді таңдаңыз
5. Конфигурациялау:
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `python kazakh_literature_bot.py`
   - **Port**: `8000`

### Қадам 3: Secrets орнату

Koyeb Dashboard-та:
1. **Settings** → **Secrets**
2. Жаңа secret қосыңыз:
   - **Name**: `BOT_TOKEN`
   - **Value**: Ваш Telegram bot token

### Қадам 4: Deploy

```bash
# Автоматты deploy GitHub push-та
git push origin main
```

---

## 🎨 Render-ге орнату

### Қадам 1: Render-де сервис жасау

1. [Render.com](https://render.com) сайтына кіріңіз
2. **New +** → **Web Service**
3. GitHub репозиторийіңізді таңдаңыз
4. Конфигурациялау:
   - **Name**: `kazakh-literature-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python kazakh_literature_bot.py`

### Қадам 2: Environment Variables

Render Dashboard-та:
1. **Environment** табын ашыңыз
2. Жаңа variable қосыңыз:
   - **Key**: `BOT_TOKEN`
   - **Value**: Ваш Telegram bot token

### Қадам 3: Deploy

```bash
git push origin main
```

---

## 🐳 Docker-мен орнату

### Локалды Docker-мен

```bash
# Docker image жасау
docker build -t kazakh-literature-bot .

# Container іске қосу
docker run -e BOT_TOKEN=your_token_here \
           -p 8000:8000 \
           kazakh-literature-bot
```

### Docker Compose-мен

```bash
# .env файлын дайындаңыз
cp .env.example .env
# BOT_TOKEN-ді қосыңыз

# Сервистерді іске қосу
docker-compose up -d

# Логтарды көру
docker-compose logs -f bot

# Сервистерді тоқтату
docker-compose down
```

### Docker Hub-та публикациялау

```bash
# Docker Hub-та логин
docker login

# Image-ді tag-тау
docker tag kazakh-literature-bot:latest your-username/kazakh-literature-bot:latest

# Push
docker push your-username/kazakh-literature-bot:latest
```

---

## 🧪 Локалды тестілеу

### Unit тестілер

```bash
# Барлық тестілерді іске қосу
pytest tests/ -v

# Белгілі бір тестті іске қосу
pytest tests/test_bot.py::TestDatabase -v

# Coverage есебін алу
pytest tests/ --cov=. --cov-report=html
```

### Интеграция тестілері

```bash
# Интеграция тестілерін іске қосу
pytest tests/ -m integration -v
```

### Өндіріс тестілері

```bash
# Өндіріс тестілерін іске қосу
pytest tests/ -m performance -v
```

### Қауіпсіздік тестілері

```bash
# Қауіпсіздік тестілерін іске қосу
pytest tests/ -m security -v
```

### Локалды бот тестілеу

```bash
# Бот іске қосу
python kazakh_literature_bot.py

# Telegram-та @BotFather арқылы жасалған ботыңызға хабарлама жіберіңіз
# /start командасын пайдаланыңыз
```

---

## 📊 Мониторинг және логирование

### Логтарды көру

```bash
# Локалды логтар
tail -f bot.log

# Docker логтары
docker logs -f kazakh-literature-bot

# Koyeb логтары
# Koyeb Dashboard → Logs табы

# Render логтары
# Render Dashboard → Logs табы
```

### Health Check

```bash
# Health check endpoint
curl http://localhost:8000/health

# Koyeb/Render автоматты health check
# Әрбір 30 секундта /health endpoint-ін тексереді
```

### Мониторинг метрикалары

- **Uptime**: Сервис қосылу уақыты
- **Response Time**: Жауап уақыты
- **Error Rate**: Қате пайызы
- **CPU Usage**: CPU пайдалану
- **Memory Usage**: Жадын пайдалану

---

## 🔒 Қауіпсіздік

### Best Practices

1. **Secrets Management**
   - `.env` файлын `.gitignore`-та сақтаңыз
   - Құпиялар платформаның secrets менеджерінде сақталсын
   - Құпиялар логтарда көрсетілмесін

2. **Token Rotation**
   - Регулярлы token-ді өзгертіңіз
   - Ескі token-ді деактивтеңіз

3. **Rate Limiting**
   - Telegram API rate limits-ін сақтаңыз
   - Пайдаланушы сұрақтарын лимиттеңіз

4. **Input Validation**
   - Барлық пайдаланушы мәліметін тексеріңіз
   - SQL injection-ге қарсы қорғаныңыз

5. **HTTPS**
   - Webhook үшін HTTPS пайдаланыңыз
   - SSL сертификатын орнатыңыз

### Қауіпсіздік аудиті

```bash
# Құпиялар тексеру
grep -r "BOT_TOKEN" --include="*.py" .

# Зависимостілерді тексеру
pip audit

# Код сканирлеу
bandit -r kazakh_literature_bot.py
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
# Автоматты тестілеу және deployment
```

**Pipeline қадамдары:**
1. ✅ Unit тестілер
2. ✅ Интеграция тестілері
3. ✅ Код сканирлеу
4. ✅ Docker image жасау
5. ✅ Koyeb/Render-ге deploy

---

## 🆘 Troubleshooting

### Бот іске қосылмайды

```bash
# BOT_TOKEN тексеру
echo $BOT_TOKEN

# Зависимостілерді қайта орнату
pip install -r requirements.txt --force-reinstall

# Логтарды көру
tail -f bot.log
```

### Telegram-та жауап беріп жатқан жоқ

```bash
# Бот іске қосылғанын тексеру
ps aux | grep kazakh_literature_bot

# Портты тексеру
netstat -an | grep 8000

# Firewall тексеру
sudo ufw status
```

### Memory leak

```bash
# Memory пайдалануын мониторинг
watch -n 1 'ps aux | grep kazakh_literature_bot'

# Docker memory лимиті
docker run -m 512m kazakh-literature-bot
```

---

## 📞 Қолдау

Сұрақтарыңыз болса:
- 📧 Email: support@example.com
- 💬 Telegram: @kazakh_literature_bot
- 🐛 Issues: GitHub Issues

---

## 📝 Лицензия

MIT License - Толық ақпарат үшін LICENSE файлын қараңыз

---

**Соңғы өндіктеу:** 8 апреля 2026 г.
**Версия:** 4.0
