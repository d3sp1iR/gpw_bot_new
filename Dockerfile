FROM python:3.11-slim

WORKDIR /

COPY . .
RUN pip install --no-cache-dir pyTelegramBotAPI
COPY . .

CMD ["python", "-u", "bot.py"]