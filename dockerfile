FROM python:3.12.4

WORKDIR /api-schoolsystem-entregavel3

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python", "/api-schoolsystem-entregavel3/app.py"]

