# Flask-leaderboard

This project is created to run a simple leaderboard api for a prediction type machine learning competition. The product of the API is a leaderboard which can be visited on the root route of the webapplication. All other communication with the API is done through a rest-API.

The key features of the API are:

* Submissions are sent directly from python code
* The Submissions are only evaluated daily to avoid overfit 
* Each team can only submit 5 times
* The master record, i.e. the ground truth, can be dynamically as well as the finaldate for submission

# Usage

* Clone project
* Create an instance folder with a config.py
* Set your application details in "instance/config.py" (see config.py in root for options)
* Test by running app.py
* Deploy by creating a docker file (see flask.dockerfile)
* Communication with the API is described in test.py
