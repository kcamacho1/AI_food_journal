from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from models import db, FoodEntry
from Utils.routes import food_entry_routes, routes, spiritual_playlist_routes, exercise_log_routes
from Utils.food_journal import food_journal_routes
from Utils.actions import actions_routes
from config import COOKIE_KEY
import os

# Initialize app
app = Flask(__name__)
app.secret_key = COOKIE_KEY  # Generates a new random key every time


# Setup database config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#initialize databse
db.init_app(app)

##Home
@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('home.html')

##Routes
app.register_blueprint(routes) # Regular Routes
app.register_blueprint(food_journal_routes) #Display Stats
app.register_blueprint(food_entry_routes) #Food Entry Methods
app.register_blueprint(exercise_log_routes) #Exercise Logs
app.register_blueprint(spiritual_playlist_routes) #Spiritual playlist
app.register_blueprint(actions_routes) #Delete/Edit


# Ensure DB exists and run app
if __name__ == '__main__':
    if not os.path.exists("database.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True)