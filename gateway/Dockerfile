FROM python:3.9-slim-buster

WORKDIR /gateway

COPY requirements.txt /gateway/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /gateway/requirements.txt
COPY ./server /gateway/server
COPY ./secrets /gateway/secrets

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
