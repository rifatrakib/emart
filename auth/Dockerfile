FROM python:3.9-slim-buster

WORKDIR /auth

COPY requirements.txt /auth/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /auth/requirements.txt
COPY ./server /auth/server
COPY ./secrets /auth/secrets

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
