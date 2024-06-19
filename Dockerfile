# 
FROM python:3.10-slim

WORKDIR /app

COPY . /app 

COPY requirements.txt .
RUN pip install -r requirements.txt


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]