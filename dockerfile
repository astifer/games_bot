FROM python:3.10.10-alpine

RUN mkdir /bot
RUN touch log.txt

COPY requirements.txt /bot
COPY log.txt /bot

WORKDIR /bot

RUN pip install -r requirements.txt

COPY . /bot

CMD ["python", "main.py"]