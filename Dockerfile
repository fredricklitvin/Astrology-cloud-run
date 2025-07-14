
FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]
