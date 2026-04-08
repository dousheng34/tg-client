# 🤝 ЫНАМДАСТЫРУ ҚҰЖАТЫ
## Қазақ Әдебиеті Telegram Боты v4.0

Бізге ынамдастыруға қызығушылық танытқаныңыз үшін рахмет! 🎉

---

## 📋 Мазмұны
1. [Кодекс](#кодекс)
2. [Ынамдастыру процесі](#ынамдастыру-процесі)
3. [Кодты жазу стилі](#кодты-жазу-стилі)
4. [Commit хабарламалары](#commit-хабарламалары)
5. [Pull Request процесі](#pull-request-процесі)
6. [Тестілеу](#тестілеу)
7. [Құжаттау](#құжаттау)

---

## 📜 Кодекс

### Біздің承諾
Біз барлық ынамдастырушыларға құрметтеу, инклюзивтілік және қауіпсіздік орта құруға міндеттіміз.

### Ынамдастырушылар үшін ережелер
- ✅ Басқаларға құрметпен қарау
- ✅ Құрметтеу және инклюзивтілік
- ✅ Конструктивті критика
- ✅ Қауіпсіздік және құпиялық

### Қабылдамайтын мінез
- ❌ Қорлау немесе қорқыту
- ❌ Дискриминация
- ❌ Жеке немесе сыйлы ақпаратты ашу
- ❌ Өтеу немесе қорлау

---

## 🔄 Ынамдастыру процесі

### 1. Форк жасау

```bash
# GitHub-та репозиторийді форк етіңіз
# https://github.com/your-username/kazakh-literature-bot/fork
```

### 2. Клон жасау

```bash
git clone https://github.com/your-username/kazakh-literature-bot.git
cd kazakh-literature-bot
```

### 3. Ветка жасау

```bash
# Develop веткасынан жаңа ветка жасаңыз
git checkout -b feature/your-feature-name
# немесе
git checkout -b fix/your-bug-fix
```

### 4. Өзгерістер жасау

```bash
# Өзгерістер жасаңыз
# Тестілеңіз
# Құжаттау жасаңыз
```

### 5. Commit жасау

```bash
git add .
git commit -m "feat: Сипаттама"
```

### 6. Push жасау

```bash
git push origin feature/your-feature-name
```

### 7. Pull Request жасау

GitHub-та Pull Request жасаңыз:
- Анық сипаттама жазыңыз
- Байланысты issues-ті көрсетіңіз
- Скриншоттар қосыңыз (қажет болса)

---

## 💻 Кодты жазу стилі

### Python стилі (PEP 8)

```python
# ✅ Дұрыс
def get_user_score(user_id: int) -> Dict:
    """Пайдаланушының ұпайын алу"""
    if user_id not in user_scores:
        user_scores[user_id] = {
            "total": 0,
            "correct": 0
        }
    return user_scores[user_id]

# ❌ Қате
def getuserscore(userid):
    if userid not in user_scores:
        user_scores[userid] = {"total": 0, "correct": 0}
    return user_scores[userid]
```

### Ережелер

1. **Атау конвенциясы**
   - Функциялар: `snake_case`
   - Класстар: `PascalCase`
   - Константалар: `UPPER_SNAKE_CASE`

2. **Сызық ұзындығы**
   - Максимум 100 символ
   - Логикалық сызықтарды бөліңіз

3. **Импорттар**
   - Стандартты библиотека
   - Үшінші тарап
   - Локалды модульдер

4. **Docstrings**
   ```python
   def function_name(param: Type) -> ReturnType:
       """Қысқа сипаттама.
       
       Ұзақ сипаттама (қажет болса).
       
       Args:
           param: Параметр сипаттамасы
       
       Returns:
           Қайтарылатын мәнің сипаттамасы
       
       Raises:
           ExceptionType: Қандай жағдайда ыстау болатыны
       """
   ```

5. **Type Hints**
   ```python
   from typing import Dict, List, Optional
   
   def process_data(data: List[str]) -> Dict[str, int]:
       """Деректерді өңдеу"""
       pass
   ```

---

## 📝 Commit хабарламалары

### Формат

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Түрлері

- **feat**: Жаңа ерекшелік
- **fix**: Қате түзету
- **docs**: Құжаттау өзгерістері
- **style**: Код стилі өзгерістері
- **refactor**: Код рефакторинг
- **perf**: Өндіріс оңтайландыру
- **test**: Тестілер қосу немесе өзгерту
- **chore**: Build, dependencies және т.б.

### Мысалдар

```bash
# ✅ Дұрыс
git commit -m "feat(quiz): Викторина сұрақтарын қосу"
git commit -m "fix(bot): Авторлар көрсетілмеген қатесін түзету"
git commit -m "docs: README.md-ді жаңарту"

# ❌ Қате
git commit -m "fixed stuff"
git commit -m "WIP"
git commit -m "asdf"
```

---

## 🔀 Pull Request процесі

### PR сипаттамасы

```markdown
## Сипаттама
Бұл PR не істейді?

## Түрі
- [ ] Жаңа ерекшелік
- [ ] Қате түзету
- [ ] Құжаттау өзгерістері

## Байланысты Issues
Closes #123

## Өзгерістер
- Өзгеріс 1
- Өзгеріс 2

## Тестілеу
Қалай тестілеуге болады?

## Скриншоттар (қажет болса)
[Скриншоттарды қосыңыз]

## Checklist
- [ ] Кодты өзім тестіледім
- [ ] Құжаттау жасадым
- [ ] Commit хабарламалары анық
- [ ] Өзгерістер бір ерекшелік үшін
```

### PR рецензиясы

Рецензиялау кезінде:
- ✅ Кодты оқыңыз
- ✅ Логиканы тексеріңіз
- ✅ Тестілерді тексеріңіз
- ✅ Құжаттауды тексеріңіз
- ✅ Конструктивті пікір беріңіз

---

## 🧪 Тестілеу

### Тестілеу өндіктемелері

```bash
# Барлық тестілерді іске қосу
pytest tests/ -v

# Белгілі бір файлды тестілеу
pytest tests/test_bot.py -v

# Coverage есебін алу
pytest tests/ --cov=. --cov-report=html

# Белгілі бір тестті іске қосу
pytest tests/test_bot.py::TestDatabase::test_database_structure -v
```

### Тестілеу ережелері

1. **Барлық жаңа кодта тестілер болуы керек**
   - Минимум 80% coverage
   - Unit тестілер
   - Интеграция тестілері

2. **Тестілер анық болуы керек**
   ```python
   def test_add_score_increases_total():
       """Ұпай қосу барлығы ұпайын өсіреді"""
       user_id = 123
       initial_score = get_user_score(user_id)["total"]
       add_score(user_id, 10)
       final_score = get_user_score(user_id)["total"]
       assert final_score == initial_score + 10
   ```

3. **Тестілер тез болуы керек**
   - Максимум 1 сек бір тест
   - Mock-ты пайдаланыңыз

---

## 📚 Құжаттау

### Құжаттау ережелері

1. **README.md**
   - Жобаның сипаттамасы
   - Орнату нұсқаулығы
   - Қолдану мысалдары

2. **Docstrings**
   - Барлық функциялар
   - Барлық класстар
   - Барлық модульдер

3. **Комментарийлер**
   - Күрделі логика
   - Бизнес ережелері
   - Ынамдастырушы ескертпелері

4. **CHANGELOG.md**
   ```markdown
   ## [4.0] - 2026-04-08
   ### Added
   - Жаңа ерекшелік
   
   ### Fixed
   - Қате түзету
   
   ### Changed
   - Өзгеріс
   ```

---

## 🔍 Кодты сканирлеу

### Linting

```bash
# Flake8 пайдаланыңыз
flake8 kazakh_literature_bot.py

# Black пайдаланыңыз
black kazakh_literature_bot.py

# isort пайдаланыңыз
isort kazakh_literature_bot.py
```

### Type Checking

```bash
# mypy пайдаланыңыз
mypy kazakh_literature_bot.py
```

### Security

```bash
# bandit пайдаланыңыз
bandit -r kazakh_literature_bot.py
```

---

## 🚀 Release процесі

### Версиялау

Semantic Versioning пайдаланамыз: `MAJOR.MINOR.PATCH`

- **MAJOR**: Үйлесімсіз өзгерістер
- **MINOR**: Артқа үйлесімді жаңа ерекшеліктер
- **PATCH**: Артқа үйлесімді қате түзетулер

### Release қадамдары

```bash
# Версияны өндіктеңіз
# CHANGELOG.md-ді жаңартыңыз
# Commit жасаңыз
git commit -m "chore: v4.1.0 release"

# Tag жасаңыз
git tag -a v4.1.0 -m "Release v4.1.0"

# Push жасаңыз
git push origin main --tags
```

---

## 📞 Қолдау

Сұрақтарыңыз болса:
- 💬 Discussions: GitHub Discussions
- 🐛 Issues: GitHub Issues
- 📧 Email: support@example.com

---

## 📄 Лицензия

Бұл жобаға ынамдастыру арқылы сіз MIT лицензиясына келісесіз.

---

**Рахмет сіздің ынамдастыруыңыз үшін!** 🙏

