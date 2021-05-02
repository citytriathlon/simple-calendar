FROM python:3.9

EXPOSE 8000

WORKDIR /

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirments.txt

CMD ["python3 techscenar/manage.py run techscenar"]
