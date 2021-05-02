FROM python:3.9

EXPOSE 8000

WORKDIR techscenar

RUN pip3 install -r requirments.txt
