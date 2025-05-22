from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from models import db, FoodEntry
from Utils.food_entry import food_entry_routes
from Utils.actions import actions_routes
from Utils.display_stats import display_stats_routes
from dotenv import load_dotenv
import os


#TODO
##

# Homepage:   [] Center New Nav buttons
# Food Entry: [] Display 3 options [manual, scan, upload]
########      [] Remove 'Food Scanner' title
#####         [] Onclick 'Manual' > Food Entry Form
#             [] Onclick 'Scan' > 
#                   [] Open Camera and scan image/barcode
##                  [] Get food item and serving size and nutritional profile
###                 [] Save in Food Journal Database
#             [] Onclick 'Upload' 
#                   [] Allow user image upload
##                  [] Get food item name and serving size and nutritional profile
###                 [] Save in Food Journal Database
#             [] Onclick 'Manual' 
#                   [] Get user form entry [Food item, serving size]
##                  [] Save to database
###                 [] Get Nutritional Profile
# Statistics and Logs: 
##            [x] Display table of Food entries
###           [] Display Graph of user data vs RDA



# Initialize app
app = Flask(__name__)
load_dotenv()

# Setup database config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#initialize databse
db.init_app(app)

##Home
@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('index.html')

##Routes
app.register_blueprint(food_entry_routes) #Food Entry Methods
app.register_blueprint(display_stats_routes) #Display Stats
app.register_blueprint(actions_routes) #Delete/Edit


# Ensure DB exists and run app
if __name__ == '__main__':
    if not os.path.exists("database.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True)