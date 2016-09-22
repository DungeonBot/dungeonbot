# -*- coding: utf-8 -*-
"""Configure the Flask app."""

import os
from flask import Flask


################################
# APP CONFIG
#################################

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_CRED = DB_USER + ":" + DB_PASS
DB_NAME = "dungeonbot_db"
DB_URL = "postgresql://" + DB_CRED + "@localhost/" + DB_NAME

app = Flask(__name__)
app.config.update(
    DEBUG=os.getenv("DEBUG", False),
    SECRET_KEY=os.getenv("SECRET_KEY", "sooper seekrit"),
    SQLALCHEMY_DATABASE_URI=DB_URL,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
