FROM python:3.9-slim-buster

WORKDIR /auth

COPY . /auth
RUN pip install --no-cache-dir --upgrade -r /auth/requirements.txt

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
