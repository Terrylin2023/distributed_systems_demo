From python:3.10
RUN pip install Flask influxdb-client
WORKDIR /app
COPY . /app
CMD ["python", "app.py"]
