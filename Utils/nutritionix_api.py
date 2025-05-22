import requests
import os

NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")

def get_nutrition_data(food_name):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "query": food_name
    }

    reponse = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        nutrients = response.json()["foods"][0]
        return {
            "calories": nutrients.get("nf_calories"),
            "protein": nutrients.get("nf_protein"),
            "fat": nutrients.get("nf_total_fat"),
            "carbs": nutrients.get("nf_total_carbohydrate"),
            "name": nutrients.get("nf_name")
        } 
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None