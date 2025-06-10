# Utils/nutrition_gaps.py

import openai
import os

# Load API key (set this in your .env!)
openai.api_key = os.getenv("OPENROUTER_API_KEY")  # Set this in your .env
openai.api_base = "https://openrouter.ai/api/v1"

# Example RDA values — you can expand this
RDA = {
    "calories": 2000,
    "protein": 50,  # grams
    "carbs": 130,    # grams
    "fat": 77 # grams
    # Add more nutrients here
}

# Rule-based food suggestions
nutrient_suggestions = {
    "calories": ["chicken thighs", "potatoes", "greek yogurt", "eggs", "salmon"],
    "protein": ["chicken breast", "tofu", "greek yogurt", "eggs", "salmon"],
    "carbs": ["rice", "squash", "potatoes", "sweet potatoes", "pasta"],    
    "fat": ["coconut oil", "olive oil", "avocado", "egg yolk", "salmon"],
}

def analyze_gaps(user_intake):
    gaps = []
    for nutrient, rda_value in RDA.items():
        intake_value = user_intake.get(nutrient, 0)
        if intake_value < rda_value * 0.8:
            gaps.append(nutrient)
    return gaps

def suggest_foods(gaps):
    suggestions = {}
    for gap in gaps:
        suggestions[gap] = nutrient_suggestions.get(gap, ["No suggestions available"])
    return suggestions

def gemini_analyze_nutrition(food_log, user_intake, rda_totals, period):
    intake_summary = "\n".join([f"{nutrient}: {amount} vs RDA {rda_totals[nutrient]}" for nutrient, amount in user_intake.items()])

    prompt = f"""
You are a nutrition coach.

Here is a user's food log over the past {period}:

{food_log}

Here is a summary of their nutrient intake vs the cumulative RDA for {period}:

{intake_summary}

Please analyze this data and answer:

1. Which nutrients are significantly under target?  
2. Which nutrients are over target?  
3. What general advice would you give this user to balance their nutrition over this period?  
4. Suggest 3 practical improvements they could make in the next {period}.  

Respond clearly and concisely.
"""

    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text
