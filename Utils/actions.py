#######################
## Actions Functions ##
#######################

from flask import Blueprint, render_template, redirect, request
from models import FoodEntry, db
from Utils.nutritionix_api import get_nutrition_data


actions_routes = Blueprint('actions_routes', __name__)

# Delete an entry
@actions_routes.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id: int):
    delete_entry = FoodEntry.query.get_or_404(id)
    try:
        db.session.delete(delete_entry)
        db.session.commit()
        return redirect("/display_stats")
    except Exception as e:
        return f"ERROR: {e}"

# Edit an entry
@actions_routes.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_food(id):
    entry = FoodEntry.query.get_or_404(id)

    if request.method == "POST":
        # 1. Get new user input
        qty = request.form.get("serving_qty")
        unit = request.form.get("serving_unit")
        query = f"{qty} {unit} {entry.food}"

        # 2. Call Nutritionix
        updated = get_nutrition_data(query)

        if updated:
            entry.serving_qty = updated["serving_qty"]
            entry.serving_unit = updated["serving_unit"]
            entry.calories = updated["nf_calories"]
            entry.protein = updated["nf_protein"]
            entry.fat = updated["nf_total_fat"]
            entry.carbs = updated["nf_total_carbohydrate"]
            db.session.commit()
            return redirect("/display_stats")
        else:
            return "Error updating nutrition data", 500

    return render_template("edit.html", entry=entry)
