import sqlite3
from flask import g
import json


DATABASE = "data/leaderboard.db"
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource('db_schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def commit_db(query, args=()):
    db = get_db()
    db.execute(query, args)
    db.commit()

def get_users():
    return query_db("SELECT user,hash FROM users")

def get_user(user):
    return query_db("SELECT user,hash FROM users "
                    "WHERE user=?", (user,), True)

def add_user(user, hash):
    commit_db("INSERT INTO users(user,hash) VALUES(?,?)", (user, hash))

def get_submissions(user = None, datetime_id = None):
    return query_db("SELECT user, datetime_id, accuracy, f1, auc, ap, prediction, note "
                    "FROM submissions "
                    "WHERE (user=:user OR :user IS NULL) "
                    "AND (datetime_id=:datetime_id OR :datetime_id IS NULL)",
                    {"user": user, "datetime_id": datetime_id})

def add_submission(user, datetime_id, accuracy, f1, auc, ap, prediction, note):
    prediction = json.dumps(prediction)
    query = "INSERT INTO submissions(user, datetime_id, accuracy, f1, auc, ap, prediction, note) " \
            "VALUES(?,?,?,?,?,?,?,?)"
    commit_db(query, (user, datetime_id, accuracy, f1, auc, ap, prediction, note))

def update_submission(user, datetime_id, accuracy, f1, auc, ap, prediction, note):
    prediction = json.dumps(prediction)
    commit_db("UPDATE submissions "
              "SET accuracy=:accuracy, f1=:f1, auc=:auc, ap=:ap, prediction=:prediction, note=:note "
              "WHERE user=:user AND datetime_id=:datetime_id",
              {"user": user, "datetime_id": datetime_id, "accuracy": accuracy, "f1": f1, "auc": auc, "ap": ap,
               "prediction": prediction, "note": note})

def clear_all_leaderboard_data():
    db = get_db()
    db.execute("DELETE FROM submissions")
    db.execute("DELETE FROM users")
    db.commit()

def set_finaldate(datetime_text):
    commit_db("UPDATE master_record "
              "SET final_date=?", [datetime_text,])

def get_finaldate():
    row=query_db("SELECT final_date "
                 "FROM master_record", (), True)
    return row["final_date"]

def set_ytrue(y_true):
    json_data = json.dumps(y_true)

    commit_db("UPDATE master_record "
              "SET y_true=?", [json_data,])

def get_ytrue():
    row=query_db("SELECT y_true "
                 "FROM master_record", (), True)
    return json.loads(row["y_true"])


def get_number_of_submissions(user):
    row = query_db("SELECT count(*) "
                   "FROM submissions "
                   "WHERE user=?", (user, ), True)["count(*)"]
    return row


if __name__ == '__main__':
    from app import create_app
    app = create_app()
