FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y supervisor

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN alembic upgrade head

CMD ["python", "app.py"]