from datetime import datetime

def get_current():
    return (datetime.today().date() - datetime.strptime("20220101", "%Y%m%d").date()).days
