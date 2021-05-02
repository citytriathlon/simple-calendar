FROM python:3-buster

EXPOSE 8000

WORKDIR /

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirments.txt

CMD ["python", "./techscenar/manage.py", "runserver", "0.0.0.0:8000"]
