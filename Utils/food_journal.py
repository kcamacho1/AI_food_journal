##############################
## Food Journal with Charts ##
##############################

from flask import Blueprint, render_template, redirect, request
from models import FoodEntry, db

food_journal_routes = Blueprint('food_journal_routes', __name__)

@food_journal_routes.route("/food_journal", methods=["GET", "POST"])
def food_journal():
    entries = FoodEntry.query.order_by(FoodEntry.date.desc()).all()
    return render_template('food_journal.html', entries=entries)