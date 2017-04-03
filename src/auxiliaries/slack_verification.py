# -*- coding: utf-8 -*-

"""
A tiny Flask app to verify the URL for Slack's Events API.
"""

from flask import Flask, Response, request


################################
# APP SETTINGS
################################

app = Flask(__name__)


################################
# API ROUTES
################################

@app.route("/", methods=["POST"])
def verify():
    challenge = request.json['challenge']
    return Response(
        response="challenge: " + challenge,
        status=200,
        headers={
            "Content-type": "application/x-www-form-urlencoded",
        },
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
