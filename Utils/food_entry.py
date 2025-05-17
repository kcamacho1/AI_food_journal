#####################
## Food Entry Page ##
#####################

from flask import Blueprint, render_template, redirect, request
from models import MyEntry, db

food_entry_routes = Blueprint('food_entry_routes', __name__)

## Manual Entry
@food_entry_routes.route("/manual_entry", methods=["GET", "POST"])
def manual_entry():
    if request.method == "POST":
        food = request.form.get('food')
        serving_size = request.form.get('serving_size')

        if food and serving_size:
            new_entry = MyEntry(
                food=food,
                serving_size=int(serving_size),
                protein=0,
                fat=0,
                carbs=0
            )
            try:
                db.session.add(new_entry)
                db.session.commit()
                return redirect("display_stats_routes.display_stats")
            except Exception as e:
                return f"ERROR: {e}"
        else:
            return "Food and Serving Size are required."
    else:
        return render_template('food_entry.html')

## Food Scanner
@food_entry_routes.route("/scan_food", methods = ["POST", "GET"])
def scan_food():
    return render_template('scan_food.html')

## Upload Image
@food_entry_routes.route("/upload_image", methods = ["POST", "GET"])
def upload_image():
    return render_template('upload_image.html')