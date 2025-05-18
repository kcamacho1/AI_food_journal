###################
## Nutrition Api ##
###################
import requests
from config import NUTRITIONIX_API_KEY, NUTRITIONIX_APP_ID

# Nutrition API
def fetch_nutrition_data(query):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"query": query, "timezone": "US/Eastern"}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
