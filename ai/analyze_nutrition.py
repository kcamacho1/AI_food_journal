import openai
import os


# Basic RDA for now - to be expanded on later
RDA = {
    "calories": 2000,
    "protein": 50,
    "carbs": 275,
    "fat": 65
}

def build_nutrition_prompt(food_log, user_intake, rda_totals, period_desc):
    intake_summary = "\n".join([f"{nutrient}: {user_intake[nutrient]} / {rda_totals[nutrient]}" for nutrient in user_intake])

    prompt = f"""
You are a nutrition and wellness coach.

Here is the user's meal log for the period: {period_desc}.

Meals consumed:
{food_log}

Summary of nutrient intake for this period vs. cumulative recommended daily allowance (RDA):

{intake_summary}

Please answer:

1. Which macronutrients or key vitamins appear to be deficient or under target?
2. Which ones are over target?
3. What 3 meal suggestions would you recommend to help balance their nutrition over the next few days?
4. What key vitamins or supplements might be helpful for this user to focus on based on this intake?
5. Provide the advice in clear bullet points.

Respond concisely and compassionately knowing the difficulty this journey takes a person on and recognizing the achievements in the individual.
"""

    return prompt

def call_openrouter(prompt):
    # Create client inside function → avoids "api_key not set" error
    client = openai.OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=[
            {"role": "system", "content": "You are a helpful nutrition and wellness coach."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )
    return response.choices[0].message.content