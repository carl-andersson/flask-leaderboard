from flask import jsonify, make_response, request, abort, render_template, escape, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

from accuracy_table import *
import datetime_id

from datetime import datetime
import numpy as np
import sklearn.metrics as skl_metrics
import database

from blueprint import api

auth = HTTPBasicAuth()
auth_admin = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    row = database.get_user(username)
    if row is not None and check_password_hash(row["hash"], password):
        return username

@auth_admin.verify_password
def verify_password(username, password):
    print(current_app.config)
    if username == current_app.config["ADMIN"] and check_password_hash(current_app.config["ADMIN_PASSWORD_HASH"], password):
        return username


@api.route('/')
def index():
    return get_leaderboard()

@api.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    submissions = database.get_submissions()
    table = []
    current_datetime_id = datetime_id.get_current()
    for submission in submissions:
        if submission["datetime_id"] < current_datetime_id:
            table.append(AccItem(escape(submission["user"]), submission["accuracy"], submission["f1"], submission["auc"],
                                        submission["ap"], escape(submission["note"])))
        else:
            table.append(AccItem(escape(submission["user"]), "TBC", "TBC", "TBC", "TBC", escape(submission["note"])))

    table.sort(key=lambda x: x.f1 if type(x.f1) != str else 0, reverse=True)

    finaldate = database.get_finaldate()
    if finaldate:
        finaldate = datetime.strptime(finaldate, "%Y%m%d").date()
    return render_template("leaderboard.html", leaderboard=AccTable(table).__html__(), finaldate=finaldate,
                           todaydate=datetime.now().date())


@api.route('/register', methods=["PUT"])
def put_team():
    team_id = request.authorization["username"]
    password = request.authorization["password"]
    if team_id == current_app.config["ADMIN"]:
        abort(400)

    if len(team_id) > 20:
        abort(400, description="Team id is too long")

    row = database.get_user(team_id)
    if row is None:
        database.add_user(team_id, generate_password_hash(password))
        return make_response("Team: " + team_id + " is now registered. Good Luck!", 201)
    else:
        if check_password_hash(row["hash"], password):
            return make_response("", 200)
        else:
            abort(400, description="Team: " + team_id + " is already registered with a different password")


@api.route('/masterrecord', methods=["PUT"])
@auth_admin.login_required
def put_masterrecord():
    if not request.json:
        abort(400)
    if type(request.json) != list:
        abort(400)

    y_true = request.json
    database.set_ytrue(y_true)

    return make_response("Master record updated", 200)

@api.route('/finaldate', methods=["PUT"])
@auth_admin.login_required
def put_finaldate():
    if request.json is None or type(request.json) != dict:
        abort(400)

    if request.json["date"]:
        date = request.json["date"]
        try:
            date = datetime.strptime(date, "%Y%m%d").date()
            date = date.strftime("%Y%m%d")
        except:
            abort(400, description="Invalid format on date")
    else:
        date = ""

    database.set_finaldate(date)
    return make_response("Master record updated to: "+ date if date else "(empty)", 200)


@api.route('/reset_leaderboard', methods=["GET"])
@auth_admin.login_required
def put_reset_leaderboard():
    database.clear_all_leaderboard_data()
    return make_response("Leaderboard reset", 200)


@api.route('/leaderboard', methods=["PUT"])
@auth.login_required
def put_leaderboard():
    team_id = auth.username()
    update = False

    if not request.json:
        abort(400)
    if 'prediction' not in request.json or type(request.json['prediction']) != list:
        abort(400, description="Submission does not contain a correctly formatted prediction")

    if 'note' not in request.json or type(request.json['note']) != str:
        request.json["note"] = ""

    if len(request.json["note"]) > 20:
        abort(400, description="Note is too long")

    today = datetime.now().strftime("%Y%m%d")
    final_date = database.get_finaldate()
    if final_date:
        if datetime.strptime(today, "%Y%m%d").date() > datetime.strptime(final_date, "%Y%m%d").date():
            abort(400, description="Submission closed")


    prediction = np.array(request.json["prediction"])
    y_true = np.array(database.get_ytrue())

    if len(y_true.shape) == 2:
        n_classes = y_true.shape[1]
    else:
        n_classes = np.max(y_true)+1
        y_true = np.eye(n_classes)[y_true]


    if (len(prediction.shape) != 2 and len(prediction.shape) != 1 and n_classes != 2)  or y_true.shape[0] != prediction.shape[0] or n_classes != prediction.shape[1]:
        abort(400, description="Prediction array is not the same size as " +
                               "the true class array which have length: "+ str(y_true.shape[0])+ " and " +
                               str(n_classes) + " classes.")


    if len(prediction.shape) == 1 and n_classes == 2:
        prediction = np.stack((1-prediction, prediction), -1)




    accuracy = skl_metrics.accuracy_score(y_true.argmax(-1), prediction.argmax(-1))
    f1 = skl_metrics.f1_score(y_true.argmax(-1), prediction.argmax(-1))
    auc = skl_metrics.roc_auc_score(y_true, prediction)
    ap = skl_metrics.average_precision_score(y_true, prediction)

    current_datetime_id = datetime_id.get_current()
    submission = database.get_submissions(team_id, current_datetime_id)
    if submission:
        database.update_submission(team_id, current_datetime_id, accuracy, f1, auc, ap, prediction.tolist(), request.json['note'])
        update = True
    else:
        if database.get_number_of_submissions(team_id) >= current_app.config["MAXIMUM_SUBMISSIONS"]:
            abort(400, description="Maximum number of predictions reached")
        database.add_submission(team_id, current_datetime_id, accuracy, f1, auc, ap, prediction.tolist(), request.json['note'])

    return make_response("Submission successful", 200 if update else 201)

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


