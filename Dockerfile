# 
FROM python:3.10

WORKDIR /app

# COPY . /app 

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --host=0.0.0.0 --reload