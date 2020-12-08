FROM python:3.6.8
#RUN apt-get update && apt-get install telnet
RUN apt-get update && apt-get install netcat-traditional
#RUN update-alternatives --config nc
RUN pip install --upgrade pip

WORKDIR /app
ADD . /app

RUN pip install datadog
RUN pip install --upgrade google-cloud-logging

CMD ["python", "jobtime.py"]
