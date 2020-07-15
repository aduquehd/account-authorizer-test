FROM python:3.7-alpine
RUN apk add --no-cache bash

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN python -m pytest

CMD ["python", "cli.py"]
