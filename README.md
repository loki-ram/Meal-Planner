# 🥗 7-Day Meal Planner

A smart, weekly meal planning web app that generates a diverse and nutritionally balanced 7-day meal plan using classic algorithms!

## 📌 Features

- Creates a **7-day meal plan** (breakfast, lunch, snack, dinner)
- Uses a **sampling-based Knapsack algorithm** to ensure meals stay within a calorie limit and optimize nutritional score
- Prevents meal repetition for lunch, dinner, and snacks across days
- Suggests **extra meals** (unused breakfasts, lunches, dinners) for more variety
- Regenerate meal plans instantly with a button
- Simple, interactive web interface

## 🧠 Algorithms Used

- **Sampling-based Knapsack**: Selects meal combinations that optimize for nutritional score while staying under a daily calorie limit.
- **Variety Constraint**: Ensures no lunch, dinner, or snack is repeated on consecutive days.

## ⚙️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Data Handling**: `pandas`, `random`
- **Cross-Origin Requests**: Handled using `Flask-CORS`

## Folder Structure

```
📁 project-root
├── nutri2.csv               # Dataset of meals with calorie and score info
├── app.py                   # Flask backend with algorithm logic
├── index.html               # Front page with "Generate Plan" button
├── meal-plan.html           # Result page that shows the generated meal plan and extras
├── requirements.txt         # Python dependencies
```

## How to Run

1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask backend**  
   ```bash
   python app.py
   ```

3. **Open `index.html`** in your browser and click “Generate Plan”.

4. **View your meal plan**  
   You’ll be redirected to `meal-plan.html` to see your 7-day plan and extra meal suggestions.  
   Click the **"Regenerate Meal Plan"** button anytime for a new plan!

---

**Note:**  
- Make sure `nutri2.csv` is present and contains enough unique meals for each category (Breakfast, Other, Snacks).
- The backend must be running for the web app to fetch meal plans.
