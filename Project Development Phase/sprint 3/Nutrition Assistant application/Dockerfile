FROM python:3.10.6
WORKDIR /application
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python","./application.py"]
