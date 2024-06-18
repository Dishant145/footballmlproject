# 
FROM python:3.10-slim

WORKDIR /app

COPY . /app 

COPY requirements.txt .
RUN pip install -r requirements.txt


CMD ["fastapi", "run", "app.py", "--port", "8080"]