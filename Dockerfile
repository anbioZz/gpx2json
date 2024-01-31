FROM python:3.12.1-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY main.py /app/main.py

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]