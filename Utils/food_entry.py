#####################
## Food Entry Page ##
#####################

from flask import Blueprint, render_template, redirect, request
from models import FoodEntry, db
from Utils.nutritionix_api import get_nutrition_data
from datetime import datetime

food_entry_routes = Blueprint('food_entry_routes', __name__)


## Food Entry Homepage
@food_entry_routes.route("/food_entry", methods = ["POST", "GET"])
def food_entry():
    return render_template('food_journal.html')

## Form Entry
@food_entry_routes.route("/add_food", methods=["GET", "POST"])
def add_food():
    if request.method == "POST":
        food_input = request.form.get("food_name", "").strip()
        meal_type = request.form.get("meal_type")
        date = datetime.utcnow().date()
        if not food_input:
            return "No food name provided", 400

        nutrition = get_nutrition_data(food_input)
        if nutrition:
            new_entry = FoodEntry(
                food=nutrition["food_name"],
                serving_qty=nutrition["serving_qty"],
                serving_unit=nutrition["serving_unit"],
                calories=nutrition["nf_calories"],
                protein=nutrition["nf_protein"],
                fat=nutrition["nf_total_fat"],
                carbs=nutrition["nf_total_carbohydrate"],
                date=date,
                meal_type=meal_type
            )
            db.session.add(new_entry)
            db.session.commit()
            return redirect("/food_journal")
        else:
            return "Could not fetch nutrition data", 400

    # Show the form on GET
    return render_template("form.html")

## Food Scanner
@food_entry_routes.route("/scan_food", methods = ["POST", "GET"])
def scan_food():
    return render_template('scan_food.html')

## Upload Image
@food_entry_routes.route("/upload_image", methods = ["POST", "GET"])
def upload_image():
    return render_template('upload_image.html')

