FROM python:3.8-slim

RUN pip install flask
RUN pip install flask-table
RUN pip install flask-httpauth 
RUN pip install scikit-learn
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

#docker build -f flask.dockerfile -t leaderboard

#docker volume create leaderboard
#docker run -p 5000:5000 -v leaderboar:/data --restart unless-stopped -d leaderboard