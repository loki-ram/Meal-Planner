from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/generate-plan')
def generate_plan():
    file_path = "nutri2.csv"
    data = pd.read_csv(file_path)

    calorie_limit = 2300
    days = 7
    max_samples = 10000

    def sample_knapsack(data, calorie_limit, max_samples):
        breakfast_items = data[data['Type'] == 'Breakfast'].reset_index(drop=True)
        other_items = data[data['Type'] == 'Other'].reset_index(drop=True)
        snack_items = data[data['Type'] == 'Snacks'].reset_index(drop=True)

        selected_meals = set()
        meal_list = []

        for _ in range(max_samples):
            b = breakfast_items.sample(1).iloc[0]
            d1 = other_items.sample(1).iloc[0]
            d2 = other_items.sample(1).iloc[0]
            s = snack_items.sample(1).iloc[0]

            if d1['Meal'] == d2['Meal']:
                continue

            dishes = [b['Meal'], d1['Meal'], d2['Meal'], s['Meal']]
            if len(set(dishes)) < 4:
                continue

            total_calories = b['Calories (kcal)'] + d1['Calories (kcal)'] + d2['Calories (kcal)'] + s['Calories (kcal)']
            meal_score = b['Score'] + d1['Score'] + d2['Score']

            if total_calories <= calorie_limit and meal_score >= 15:
                meal_key = tuple(sorted(dishes))
                if meal_key not in selected_meals:
                    selected_meals.add(meal_key)
                    meal_list.append(dishes)

        return meal_list

    def arrange_meals(meals, days):
        random.shuffle(meals)
        arranged = []

        for meal in meals:
            b, l, d, s = meal

            if not arranged:
                arranged.append([b, l, d, s])
                continue

            prev_lunch, prev_dinner, prev_snack = arranged[-1][1], arranged[-1][2], arranged[-1][3]

            # Ensure lunch and dinner don't repeat from previous day, and snack doesn't repeat
            if l not in [prev_lunch, prev_dinner] and d not in [prev_lunch, prev_dinner] and s != prev_snack:
                arranged.append([b, l, d, s])

            if len(arranged) == days:
                break

        if len(arranged) < days:
            raise ValueError("Couldn't find enough non-repeating meals for all days.")

        return arranged

    try:
        selected_meals = sample_knapsack(data, calorie_limit, max_samples)

        if len(selected_meals) < days:
            return jsonify({"error": "Not enough unique meal combinations to plan for 7 days."}), 400

        arranged_meals = arrange_meals(selected_meals, days)

        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        response = [{
            "day": weekdays[i],
            "breakfast": m[0],
            "lunch": m[1],
            "snack": m[3],
            "dinner": m[2]
        } for i, m in enumerate(arranged_meals)]

        # Collect used meals
        used_breakfasts = {meal[0] for meal in arranged_meals}
        used_lunches = {meal[1] for meal in arranged_meals}
        used_dinners = {meal[2] for meal in arranged_meals}

        # Get all breakfasts, lunches, dinners from the dataset
        all_breakfasts = set(data[data['Type'] == 'Breakfast']['Meal'])
        all_lunches = set(data[data['Type'] == 'Other']['Meal'])
        all_dinners = all_lunches  # Lunch and dinner both come from 'Other'

        # Find unused meals in each category
        unused_breakfasts = list(all_breakfasts - used_breakfasts)
        unused_lunches = list(all_lunches - used_lunches)
        unused_dinners = list(all_dinners - used_dinners)

        # Pick 3 extras or less if unavailable, avoid sampling from empty lists
        extra_breakfasts = random.sample(unused_breakfasts, min(3, len(unused_breakfasts))) if unused_breakfasts else []
        extra_lunches = random.sample(unused_lunches, min(3, len(unused_lunches))) if unused_lunches else []
        extra_dinners = random.sample(unused_dinners, min(3, len(unused_dinners))) if unused_dinners else []

        response.append({
            "extras": {
                "breakfasts": extra_breakfasts,
                "lunches": extra_lunches,
                "dinners": extra_dinners
            }
        })

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)