FROM python:3.11-slim
WORKDIR /bot

COPY requirements.txt .

RUN apk add --no-cache git
RUN pip install -r requirements.txt

COPY . .

COPY .env .env

CMD ["python", "main.py"]
