FROM python:3.11-slim
WORKDIR /bot

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

COPY . .

COPY .env .env

CMD ["python", "main.py"]
