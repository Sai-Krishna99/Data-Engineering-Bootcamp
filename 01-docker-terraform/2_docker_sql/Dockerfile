FROM python:3.10.12

RUN apt-get install wget
RUN pip install pandas pyarrow sqlalchemy psycopg2

WORKDIR /app
COPY ingest-data.py ingest-data.py 

ENTRYPOINT [ "python3", "ingest-data.py" ]