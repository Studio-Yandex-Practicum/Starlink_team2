FROM python:3.12.7-alpine3.20

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["sh", "entrypoint.sh"]

