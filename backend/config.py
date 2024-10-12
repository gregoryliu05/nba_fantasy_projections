from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# start with config , then go to database

app = Flask(__name__) #setup app
CORS(app) #init cors


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nba_database.db" #specifying location of database 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) #creates database instance that give access to our database
