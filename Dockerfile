FROM python:3.8

WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt

CMD python -m task