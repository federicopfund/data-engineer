FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000

COPY . . 

CMD ["uvicorn","api:app","--reload","--host","0.0.0.0", "--port","8000"] 