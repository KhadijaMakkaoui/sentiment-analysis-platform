FROM python:3.11-slim

WORKDIR /app

# Only install what the API needs
RUN pip install flask boto3

COPY . .

CMD ["python", "app.py"]