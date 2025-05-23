#############################
## Database and Model File ##
#############################

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#blueprint to initialize database
db = SQLAlchemy()

#Our db model we want to create 
class FoodEntry(db.Model):
    __tablename__ = 'food_entry'

    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(100), nullable=False)
    serving_qty = db.Column(db.Float, nullable=True)
    serving_unit = db.Column(db.String(50), nullable=True)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)
    carbs = db.Column(db.Float, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Entry: {self.id}"