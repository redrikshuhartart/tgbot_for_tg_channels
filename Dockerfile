FROM python:3.11.6
WORKDIR /bot
COPY requirements.txt .
RUN pip install aiohttp==3.8.2 aiogram==2.25.1 environs==9.5.0 yarl==1.8.1 frozenlist==1.3.1
COPY . .
CMD ["python", "bot.py"]

