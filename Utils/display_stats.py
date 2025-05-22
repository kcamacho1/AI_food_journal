########################
## Display Stats Page ##
########################

from flask import Blueprint, render_template, redirect, request
from models import FoodEntry, db

display_stats_routes = Blueprint('display_stats_routes', __name__)

@display_stats_routes.route("/display_stats", methods=["GET", "POST"])
def display_stats():
    entries = FoodEntry.query.order_by(FoodEntry.date.desc()).all()
    return render_template('display_stats.html', entries=entries)