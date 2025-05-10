FROM python:3.11-alpine
WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY .env .env

CMD ["python", "main.py"]
