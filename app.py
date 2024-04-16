import streamlit as st
import pandas as pd


def calculate_bmi(weight, height):
  return weight / ((height / 100)**2)


def calculate_ideal_weight(height, gender):
  if gender == "Male":
    return 50 + 0.91 * (height - 152.4)
  elif gender == "Female":
    return 45.5 + 0.91 * (height - 152.4)
  else:
    return None


def calculate_ideal_body_weight(height, gender):
  if gender == "Male":
    return 50 + 0.91 * (height - 152.4)
  elif gender == "Female":
    return 45.5 + 0.91 * (height - 152.4)
  else:
    return None


def calculate_body_fat_percentage(weight, body_fat_mass):
  return (body_fat_mass / weight) * 100


def calculate_bmr(weight, height, age, gender):
  if gender == "Male":
    return 10 * weight + 6.25 * height - 5 * age + 5
  elif gender == "Female":
    return 10 * weight + 6.25 * height - 5 * age - 161
  else:
    return None


def calculate_tdee(bmr, activity_level):
  activity_factors = {
      "Sedentary": 1.2,
      "Lightly active": 1.375,
      "Moderately active": 1.55,
      "Very active": 1.725,
      "Extra active": 1.9
  }
  return bmr * activity_factors[activity_level]


def calculate_calorie_intake(tdee, goals, weight, ideal_weight):
  if "Fitness" in goals:
    if weight < ideal_weight:
      goals.append("Weight gain")
    elif weight > ideal_weight:
      goals.append("Weight loss")
  if "Weight loss" in goals:
    if "Rapid Weight Loss" in goals:
      return tdee - 1000  # Subtract 1000 kcal/day for rapid weight loss
    else:
      return tdee - 500
  elif "Weight gain" in goals:
    return tdee + 500
  elif "Fitness" in goals:
    return tdee  # No calorie adjustment for fitness goal, treat it as Ideal Weight
  else:
    return tdee


def calculate_tbw(weight, height, age, gender):
  if gender == "Male":
    k = 2.447 - 0.09516 * age + 0.1074 * height + 0.3362 * weight
  elif gender == "Female":
    k = -2.097 + 0.1069 * height + 0.2466 * weight
  else:
    return None

  return 0.3669 * k - 0.0906 * weight + 0.1074 * height + 0.2466 * weight


# Define function to read meals and their calorie counts from CSV
def read_meals_from_csv(csv_file):
  meals_df = pd.read_csv("food.csv", encoding='utf-8-sig')
  return meals_df


def generate_meal_plan(calorie_intake, meals_df):
    # Define the calorie distribution for each meal category based on the user's input calorie intake
    meal_categories = {
        "Breakfast": 0.25,
        "Lunch": 0.35,
        "Dinner": 0.3,
        "Snacks": 0.1
    }

    # Calculate the calorie allowance for each meal category based on the recommended intake
    calorie_allowance = {category: calorie_intake * percentage for category, percentage in meal_categories.items()}

    # Initialize empty lists to store selected meals for each category
    meal_plan = {category: [] for category in meal_categories}

    for index, row in meals_df.iterrows():
        meal_name = row["اسم الوجبة"]
        meal_calories = row["السعرات الحرارية"]
        meal_details = {
            "Meal": meal_name,
            "Calories": meal_calories,
            "Ingredients": row["المكونات"],
            "Weight (g)": row["الوزن (جرام)"],
            "Protein (g)": row["البروتين (جرام)"],
            "Carbohydrates (g)": row["الكربوهيدرات (جرام)"],
            "Fat (g)": row["الدهون (جرام)"],
            "Meal Type": row["نوع الوجبة"]
        }

        # Check if the meal fits into any of the categories based on remaining calorie allowance
        for category, allowance in calorie_allowance.items():
            if meal_calories <= allowance:
                # Add the meal to the corresponding category
                meal_plan[category].append({"Meal": meal_name, "Calories": meal_calories})
                # Deduct the calories of the meal from the remaining allowance for the category
                calorie_allowance[category] -= meal_calories
                break  # Move to the next meal once added to a category

    return meal_plan



def display_meal_plan(meal_plan):
  st.subheader("Daily Meal Plan:")
  for category, meals in meal_plan.items():
    st.subheader(category)
    for meal_info in meals:
      st.write(f"**{meal_info['Meal']}**: {meal_info['Calories']:.2f}    kcal")



def user_input_page():
  st.title("AI Calorie Calculator")

  # Sidebar for additional options
  st.sidebar.title("Options")

  # Age input
  age = st.sidebar.number_input("Enter your age",
                                min_value=10,
                                max_value=150,
                                step=1)

  # Gender selection
  gender = st.sidebar.selectbox("Select your gender",
                                options=["Male", "Female", "Other"])

  # Weight and height input
  st.sidebar.subheader("Weight and Height:")
  weight = st.sidebar.number_input("Enter your weight (kg)",
                                   min_value=50.0,
                                   step=1.0)
  height = st.sidebar.number_input("Enter your height (cm)",
                                   min_value=100.0,
                                   step=1.0)

  # Body composition input
  st.sidebar.subheader("Body Composition:")
  body_fat_percentage = st.sidebar.number_input(
      "Enter your body fat percentage (%)",
      min_value=0.0,
      max_value=100.0,
      step=0.1)
  waist_to_hip_ratio = st.sidebar.number_input("Enter your waist-to-hip ratio",
                                               min_value=0.0,
                                               step=0.01)
  lean_body_mass = st.sidebar.number_input("Enter your lean body mass (kg)",
                                           min_value=0.0,
                                           step=0.1)

  # Calculate BMI
  bmi = calculate_bmi(weight, height)

  # Calculate total body water (TBW)
  tbw = calculate_tbw(weight, height, age, gender)

  # Calculate ideal weight
  ideal_weight = calculate_ideal_weight(height, gender)

  # Calculate body fat mass
  body_fat_mass = weight * (body_fat_percentage / 100)

  # Calculate BMR
  bmr = calculate_bmr(weight, height, age, gender)

  # Calculate TDEE
  activity_level = st.selectbox("Select your activity level",
                                options=[
                                    "Sedentary", "Lightly active",
                                    "Moderately active", "Very active",
                                    "Extra active"
                                ])
  tdee = calculate_tdee(bmr, activity_level)

  # Dietary goals selection
  st.sidebar.subheader("Select your dietary goals:")
  weight_loss = st.sidebar.checkbox("Weight loss")
  weight_gain = st.sidebar.checkbox("Weight gain")
  maintenance = st.sidebar.checkbox("Maintenance")
  fitness = st.sidebar.checkbox("Fitness")
  rapid_weight_loss = st.sidebar.checkbox("Rapid Weight Loss")

  goals = []
  if weight_loss:
    goals.append("Weight loss")
  if weight_gain:
    goals.append("Weight gain")
  if maintenance:
    goals.append("Maintenance")
  if fitness:
    goals.append("Fitness")
  if rapid_weight_loss:
    goals.append("Rapid Weight Loss")

  # Calculate calorie intake
  calorie_intake = calculate_calorie_intake(tdee, goals, weight, ideal_weight)

  # Read meals from CSV
  meals_df = pd.read_csv("food.csv", encoding='utf-8-sig')

  # Recommended Metrics section
  st.subheader("Recommended Metrics:")
  if st.button("Show Recommended Daily Calorie Intake"):
    st.write(
        f"Recommended Daily Calorie Intake: {calorie_intake:.2f} kcal/day")

  # Display calculated metrics
  if st.button("Submit"):
    st.subheader("Calculated Metrics:")
    # BMI
    if bmi < 18.5:
      bmi_indication = "Underweight"
      st.warning(
          f"BMI: {bmi:.2f} ({bmi_indication}) - BMI is a measure of body fat based on height and weight."
      )
    elif 18.5 <= bmi < 25:
      bmi_indication = "Normal weight"
      st.success(
          f"BMI: {bmi:.2f} ({bmi_indication}) - BMI is a measure of body fat based on height and weight."
      )
    elif 25 <= bmi < 30:
      bmi_indication = "Overweight"
      st.warning(
          f"BMI: {bmi:.2f} ({bmi_indication}) - BMI is a measure of body fat based on height and weight."
      )
    else:
      bmi_indication = "Obese"
      st.error(
          f"BMI: {bmi:.2f} ({bmi_indication}) - BMI is a measure of body fat based on height and weight."
      )

    # BMR
    # There are no standard indications for BMR as it is a measure of the body's basal metabolic rate.
    st.info(
        f"BMR: {bmr:.2f} kcal/day - Basal Metabolic Rate is the amount of energy expended while at rest in a neutrally temperate environment."
    )

    # TDEE
    # You can provide interpretations based on the activity level chosen by the user.
    # For example, Sedentary, Lightly active, Moderately active, Very active, Extra active.
    st.info(
        f"TDEE: {tdee:.2f} kcal/day - Total Daily Energy Expenditure is the total number of calories burned each day."
    )

    # Body Fat Mass
    # There are no standard indications for body fat mass. It's typically interpreted in the context of overall body composition goals.
    st.info(
        f"Body Fat Mass: {body_fat_mass:.2f} kg - Body Fat Mass is the amount of fat tissue in the body."
    )

    # Total Body Water (TBW)
    # There are no standard indications for total body water. It's generally interpreted based on hydration status and health conditions.
    st.info(
        f"Total Body Water (TBW): {tbw:.2f} liters - Total Body Water is the total amount of water present in the body."
    )

    # Ideal Body Weight
    # Ideal body weight calculated using the Devine formula indicates an estimate of the weight that is considered healthy for the given height and gender.
    if gender == "Male":
      ideal_body_weight = 50 + 2.3 * (
          (height * 0.393701) - 60)  # Convert height to inches
    elif gender == "Female":
      ideal_body_weight = 45.5 + 2.3 * (
          (height * 0.393701) - 60)  # Convert height to inches
    else:
      ideal_body_weight = None

    if ideal_body_weight:
      st.info(
          f"Ideal Body Weight (Devine formula): {ideal_body_weight:.2f} kg - Ideal Body Weight is an estimate of the weight considered healthy for the given height and gender."
      )
    else:
      st.error("Unable to calculate ideal body weight: Gender not specified.")

  # Generate and display meal plan
  meal_plan = generate_meal_plan(calorie_intake, meals_df)
  display_meal_plan(meal_plan)


if __name__ == "__main__":
  user_input_page()
