FROM python:3.6
WORKDIR /app
COPY requirements.txt /app
COPY etl.py /app
COPY credentials.py /app
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "etl.py"]