FROM python:3.12.1-alpine3.19

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY main.py /app/main.py

WORKDIR /app

CMD ["python", "main.py"]