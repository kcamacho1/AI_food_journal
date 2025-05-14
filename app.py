from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

#my app
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'database.db')}"
db = SQLAlchemy(app)

#Create db
if not os.path.exists("database.db"):
    with app.app_context():
        db.create_all()

#Data class with row of data
class MyEntry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    food = db.Column(db.String(100), nullable = False)
    serving_size = db.Column(db.Integer, nullable = False)
    protein = db.Column(db.Float, nullable = True)
    fat = db.Column(db.Float, nullable = True)
    carbs = db.Column(db.Float, nullable = True)
    logged = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self)-> str:
        return f"Entry: {self.id}"

@app.route('/', methods=["POST", "GET"])
def home():
    return render_template('index.html')

#Delete an item
@app.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id:int):
    delete_entry = MyEntry.query.get_or_404(id)
    try:
        db.session.delete(delete_entry)
        db.session.commit()
        return redirect("/food_entry")
    except Exception as e:
        return f"ERROR: {e}"

@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id:int):
    entry = MyEntry.query.get_or_404(id)
    if request.method == "POST":
        entry.food = request.form.get('food')
        entry.serving_size = request.form.get('serving_size')

        if entry.food and entry.serving_size:
            try:
                db.session.add()
                db.session.commit()
                return redirect("/food_entry")
            except Exception as e:
                return f"ERROR: {e}"
        else:
            return "Food and Serving Size are required."
    else:
        return render_template('edit.html', entry=entry)       

@app.route('/food_entry', methods=["POST", "GET"])
def food_entry():
    if request.method == "POST":
        food = request.form.get('food')
        serving_size = request.form.get('serving_size')
        
        #Map fields
        new_entry = MyEntry(
            food=food,
            serving_size=int(serving_size) if serving_size else 0,
            protein=0,
            fat=0,
            carbs=0
        )

        if food and serving_size:
            new_entry = MyEntry(food=food, serving_size=int(serving_size))

            try:
                db.session.add(new_entry)
                db.session.commit()
                return redirect ("/food_entry")
            except Exception as e:
                print(f'ERROR:{e}')
                return f"ERROR: {e}"
    else:
        entries = MyEntry.query.order_by(MyEntry.logged.desc()).all()
        return render_template('food_entry.html', entries=entries)

@app.route('/scan_food')
def scan_food():
    return render_template('scan_food.html')

@app.route('/display_stats')
def display_stats():
    return render_template('display_stats.html')


# Runner and Debugger
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
