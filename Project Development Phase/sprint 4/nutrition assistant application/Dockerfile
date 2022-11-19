FROM python:3.10.6-buster
WORKDIR /application
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn","--bind","0.0.0.0:5000","app:app"]



