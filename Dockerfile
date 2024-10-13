FROM python:3.12.7-slim

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "bash", "start.sh" ]