#####################
## Food Entry Page ##
#####################

from flask import Blueprint, render_template, redirect, request, flash, send_file
from models import FoodEntry, db
from Utils.nutritionix_api import get_nutrition_data
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt


routes = Blueprint('routes', __name__)
food_entry_routes = Blueprint('food_entry_routes', __name__)
exercise_log_routes = Blueprint('exercise_log_routes', __name__)
spiritual_playlist_routes = Blueprint('spiritual_playlist_routes', __name__)





## Homepage
@routes.route("/home", methods = ["POST", "GET"])
def home():
    return render_template('home.html')

## Exercise Logger
@exercise_log_routes.route("/exercise_log", methods = ["POST", "GET"])
def exercise_log():
    return render_template('exercise_log.html')

## Spiritual playlist Page
@spiritual_playlist_routes.route("/spiritual_playlist", methods = ["POST", "GET"])
def spiritual_playlist():
    return render_template('spiritual_playlist.html')

## Food Journal and Food entry
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

## Spreadsheet Uploader

@food_entry_routes.route("/upload_spreadsheet", methods=["POST"])
def upload_spreadsheet():
    if 'spreadsheet' not in request.files:
        flash("No file part")
        return render_template('food_journal.html')

    file = request.files['spreadsheet']
    if file.filename == '':
        flash("No selected file")
        return render_template('food_journal.html')

    try:
        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext == "csv":
            df = pd.read_csv(file)
        elif ext in ["xls", "xlsx"]:
            df = pd.read_excel(file)
        else:
            flash("Unsupported file format")
            return render_template('food_journal.html')

        # Loop through each row and add to DB
        for _, row in df.iterrows():
            entry = FoodEntry(
                food=row["food"],
                calories=row["calories"],
                protein=row["protein"],
                fat=row["fat"],
                carbs=row["carbs"],
                serving_qty=row.get("serving_qty"),
                serving_unit=row.get("serving_unit"),
                date=pd.to_datetime(row.get("date", datetime.utcnow())),
                meal_type=row.get("meal_type", "unspecified")
            )
            db.session.add(entry)
        

        db.session.commit()
        flash("Spreadsheet uploaded and entries added successfully.")
    except Exception as e:
        flash(f"Upload failed: {e}")

    return render_template('food_journal.html')

## Food Scanner
@food_entry_routes.route("/scan_food", methods = ["POST", "GET"])
def scan_food():
    return render_template('scan_food.html')

## Upload Image
@food_entry_routes.route("/upload_image", methods = ["POST", "GET"])
def upload_image():
    return render_template('upload_image.html')


@food_entry_routes.route('/chart/<period>')
def chart(period):
    now = datetime.utcnow()
    if period == "day":
        start = now - timedelta(days=1)
    elif period == "week":
        start = now - timedelta(weeks=1)
    elif period == "month":
        start = now - timedelta(days=30)
    else:
        return "Invalid period", 400

    logs = FoodLog.query.filter(FoodLog.date >= start).all()
    if not logs:
        return "No data to show"

    df = pd.DataFrame([{
        "date": log.date.date(),
        "calories": log.calories,
        "protein": log.protein,
        "carbs": log.carbs,
        "fat": log.fat
    } for log in logs])

    df_grouped = df.groupby("date").sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    df_grouped.plot(kind='bar', ax=ax)
    ax.set_title(f'Nutritional Intake Over the Past {period.capitalize()}')
    ax.set_ylabel("Amount")
    ax.set_xlabel("Date")

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')