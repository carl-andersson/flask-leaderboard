FROM python:3.8-slim

COPY requirements.txt /

RUN pip install -r requirements.txt
RUN pip install waitress

COPY accuracy_table.py /
COPY view.py /
COPY app.py /
COPY blueprint.py /
COPY app_factory.py /
COPY database.py /
COPY db_schema.sql /
COPY datetime_id.py /
COPY templates /templates
COPY static /static
COPY instance /instance
COPY config.py /

ENTRYPOINT [ "waitress-serve" ]

CMD [ "--listen=0.0.0.0:5000", "app:app" ]

# Create docker file
#docker build -f flask.dockerfile -t leaderboard .

# Create a volume for persistent storage
#docker volume create leaderboard
# Run Docker file
#docker run -p 5000:5000 -p 5050:5000 -v leaderboard:/data --restart unless-stopped -d leaderboard