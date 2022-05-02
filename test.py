import requests
import json
from functools import reduce
import config

def join_slash(a, b):
    return a.rstrip('/') + '/' + b.lstrip('/')

def urljoin(*args):
    return reduce(join_slash, args) if args else ''


host = "http://"+config.HOST
admin = config.ADMIN
password = config.ADMIN_PASSWORD


def submit(team_id, password, prediction, note):
    team_id = team_id.encode('utf-8')
    password = password.encode('utf-8')
    payload = {'prediction':prediction, "note":note}
    headers = {'content-type': 'application/json'}
    r = requests.put(urljoin(host, "leaderboard"),
                     auth=(team_id, password),
                     data=json.dumps(payload), headers=headers)
    return r


def set_master(admin, password, y_true):
    payload = y_true
    headers = {'content-type': 'application/json'}
    r = requests.put(urljoin(host, "masterrecord"),
                     auth=(admin, password),
                     data=json.dumps(payload), headers=headers)
    return r

def set_finaldate(admin, password, date=None):
    # dateformat YYYYMMDD (the final date is inclusive)

    payload = {"date":date}
    headers = {'content-type': 'application/json'}
    r = requests.put(urljoin(host, "finaldate"),
                     auth=(admin, password),
                     data=json.dumps(payload), headers=headers)
    return r


def register_team(team_id, password):
    team_id = team_id.encode('utf-8')
    password = password.encode('utf-8')
    r = requests.put(urljoin(host, "register"),
                     auth=(team_id, password))
    return r

def reset_all_leaderboard_data(admin, password):
    r = requests.get(urljoin(host, "reset_leaderboard"),
                     auth=(admin, password))
    return r

def test_everything():
    r = register_team("lag1", "lag1")
    if not (r.status_code == 200 or r.status_code == 201):
        raise Exception()
    r = set_master(admin, password, (1, 0, 0, 1))
    if not (r.status_code == 200 or r.status_code == 201):
        raise Exception()
    r = set_finaldate(admin, password, "20300430")
    if not (r.status_code == 200 or r.status_code == 201):
        raise Exception()
    r = register_team("¡@£$¥{", "¡@£$¥{")
    if not (r.status_code == 200 or r.status_code == 201):
        raise Exception()
    r = submit("¡@£$¥{", "¡@£$¥{", ((0.9, 0.1), (0.9, 0.1), (0.9, 0.1), (0.9, 0.1)), "This is the note")
    if not (r.status_code == 200 or r.status_code == 201):
        raise Exception()
    r = submit("lag1", "lag1", ((0.8, 0.2), (0.8, 0.2), (0.8, 0.2), (0.8, 0.2)), "Another note")
    if not (r.status_code == 200 or r.status_code == 201):
        raise Exception()
