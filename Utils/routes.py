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
from Utils.nutrition_gaps import analyze_gaps, suggest_foods
from ai.analyze_nutrition import build_nutrition_prompt, call_openrouter, RDA
from models import FoodEntry
from datetime import datetime, timedelta
import os


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

## AI Meal Suggestions
@food_entry_routes.route("/suggest_meals", methods=["POST", "GET"])
def suggest_meals():
    # Get period from user or default to week
    period = request.args.get("period", "week")
    now = datetime.utcnow()

    if period == "day":
        start = now - timedelta(days=1)
    elif period == "week":
        start = now - timedelta(weeks=1)
    elif period == "month":
        start = now - timedelta(days=30)
    else:
        return "Invalid period", 400

    # Query DB
    entries = FoodEntry.query.filter(FoodEntry.date >= start.date()).order_by(FoodEntry.date).all()

    # Sum nutrients
    user_intake = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

    for entry in entries:
        user_intake["calories"] += entry.calories or 0
        user_intake["protein"] += entry.protein or 0
        user_intake["carbs"] += entry.carbs or 0
        user_intake["fat"] += entry.fat or 0

    # RDA totals over this period
    multiplier = {"day": 1, "week": 7, "month": 30}[period]
    rda_totals = {nutrient: RDA[nutrient] * multiplier for nutrient in RDA}

    # Build food log string for AI
    food_log = "\n".join([f"{entry.date}: {entry.meal_type or 'unspecified'} - {entry.food}" for entry in entries])
    period_desc = f"{start.date()} to {now.date()}"

    # Build prompt and call OpenRouter AI
    prompt = build_nutrition_prompt(food_log, user_intake, rda_totals, period_desc)
    ai_response = call_openrouter(prompt)

    return render_template("suggestions.html",
                           period=period,
                           period_desc=period_desc,
                           user_intake=user_intake,
                           rda_totals=rda_totals,
                           ai_response=ai_response)


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
## Spreadsheet downloader
@food_entry_routes.route("/download_template")
def download_template():
    template_path = os.path.join(os.getcwd(), "templates", "food_log_template.csv")
    return send_file(template_path, as_attachment=True)


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

    logs = FoodEntry.query.filter(FoodEntry.date >= start).all()
    if not logs:
        return "No data to show"

    df = pd.DataFrame([{
        "date": log.date(),
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