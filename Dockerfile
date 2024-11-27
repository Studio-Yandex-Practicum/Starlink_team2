FROM python:3.12

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements_dev.txt .
RUN pip install --no-cache-dir -r requirements_dev.txt

COPY . .

CMD ["python", "src/main.py"]





