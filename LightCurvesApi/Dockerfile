FROM python:3.7

COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#ENV FLASK_APP app.py
EXPOSE 5000
#CMD ["flask", "run", "--host=0.0.0.0"]

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]