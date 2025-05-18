#####################
## Food Entry Page ##
#####################

from flask import Blueprint, render_template, redirect, request
from models import MyEntry, db
from Utils.nutrition_api import fetch_nutrition_data

food_entry_routes = Blueprint('food_entry_routes', __name__)


## Food Entry Homepage
@food_entry_routes.route("/food_entry", methods = ["POST", "GET"])
def food_entry():
    return render_template('food_entry.html')

## Form Entry
@food_entry_routes.route("/form", methods=["GET", "POST"])
def form():
    data = {}
    if request.method == "POST":
        if "autofill" in request.form:
            food_query = request.form.get("food")
            result = fetch_nutrition_data(food_query)
            if result:
                food_data = result["foods"][0]
                data = {
                    "food": food_data["food_name"],
                    "serving_size": food_data["serving_qty"],
                    "protein": food_data["nf_protein"],
                    "fat": food_data["nf_total_fat"],
                    "carbs": food_data["nf_total_carbohydrate"]
                }
        elif "submit" in request.form:
            food = request.form.get("food")
            serving_size = request.form.get("serving_size")
            protein = request.form.get("protein")
            fat = request.form.get("fat")
            carbs = request.form.get("carbs")

            new_entry = MyEntry(
                food=food,
                serving_size=int(serving_size),
                protein=float(protein),
                fat=float(fat),
                carbs=float(carbs)
            )
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('food_entry_routes.form'))

    return render_template("form.html", data=data)

## Food Scanner
@food_entry_routes.route("/scan_food", methods = ["POST", "GET"])
def scan_food():
    return render_template('scan_food.html')

## Upload Image
@food_entry_routes.route("/upload_image", methods = ["POST", "GET"])
def upload_image():
    return render_template('upload_image.html')

