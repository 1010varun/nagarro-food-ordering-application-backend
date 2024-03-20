# Use an official Python runtime as a parent image
FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 4000

CMD ["python", "app.py"]
