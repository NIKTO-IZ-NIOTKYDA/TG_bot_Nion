FROM python:3.12.7-slim

WORKDIR /src

COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD [ "python3", "main.py" ]