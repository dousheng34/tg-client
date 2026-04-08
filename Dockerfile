FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY kazakh_literature_bot.py .

CMD ["python", "kazakh_literature_bot.py"]
