FROM python:3.12.7

WORKDIR /src

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./app .

CMD ["fastapi", "run", "main.py"]