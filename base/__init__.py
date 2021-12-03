from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "d641e6a403968e97b7d50ebe391c8e142825e785eec4597f5450c98ea2f2ef8e"
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@127.0.0.1:5432/sales_stock_prediction'
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'base/static/datasetfiles'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import base.com.controller
