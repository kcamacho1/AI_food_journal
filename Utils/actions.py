#######################
## Actions Functions ##
#######################

from flask import Blueprint, render_template, redirect, request
from models import FoodEntry, db

actions_routes = Blueprint('actions_routes', __name__)

# Delete an entry
@actions_routes.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id: int):
    delete_entry = MyEntry.query.get_or_404(id)
    try:
        db.session.delete(delete_entry)
        db.session.commit()
        return redirect("/food_entry")
    except Exception as e:
        return f"ERROR: {e}"

# Edit an entry
@actions_routes.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id: int):
    entry = MyEntry.query.get_or_404(id)
    if request.method == "POST":
        entry.food = request.form.get('food')
        entry.serving_size = request.form.get('serving_size')

        if entry.food and entry.serving_size:
            try:
                db.session.add(entry)
                db.session.commit()
                return redirect("/food_entry")
            except Exception as e:
                return f"ERROR: {e}"
        else:
            return "Food and Serving Size are required."
    else:
        return render_template('edit.html', entry=entry)
