FROM python:3.12-slim-bullseye

WORKDIR /gateway

COPY requirements.txt /gateway/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /gateway/requirements.txt
COPY ./server /gateway/server
COPY ./secrets /gateway/secrets

CMD ["uvicorn", "server:main", "--host", "0.0.0.0", "--port", "8000"]
