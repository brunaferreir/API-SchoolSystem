FROM python:3.12.10-slim

WORKDIR /api-schoolsystem

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python", "/api-schoolsystem/app.py"]


