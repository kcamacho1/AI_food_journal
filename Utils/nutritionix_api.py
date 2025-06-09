import requests
import os


NUTRITIONIX_API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
NUTRITIONIX_APP_ID = os.environ.get("NUTRITIONIX_APP_ID")

def get_nutrition_data(query):
    if not NUTRITIONIX_APP_ID or not NUTRITIONIX_API_KEY:
        print("❌ Nutritionix credentials are missing.")
        return None

    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json={"query": query})
    print("🧪 API response code:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        print("✅ Nutritionix result:", data["foods"][0])
        return data["foods"][0]
    else:
        print("❌ API Error:", response.status_code, response.text)
        return None