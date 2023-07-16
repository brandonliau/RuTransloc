FROM python:3.11.3-slim

WORKDIR /app

COPY ./server.py /app
COPY ./src/ /app/src
COPY ./configuration /app/configuration
COPY ./requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--reload", "--port", "8000"]