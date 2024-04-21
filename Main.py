import streamlit as st
import pandas as pd
import csv
import os
import datetime
import random



# Define the file path for storing patient data
DATA_FILE = "patient_data.csv"

# Function to save patient data
def save_patient_data(patient_data):
    fieldnames = patient_data.keys()
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        # Add current date and time to the patient data
        patient_data["datetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time
        writer.writerow(patient_data)




def calculate_bmi(weight, height):
  return weight / ((height / 100)**2)

# Function to calculate sum of numbers
def calculate_sum(numbers):
    return sum(numbers)


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
      return tdee - 500
  elif "Rapid Weight Loss" in goals:
      return tdee - 1000  # Subtract 1000 kcal/day for rapid weight loss
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



def generate_meal_plan(calorie_intake, meals_df, protein_range=None, carb_range=None, fat_range=None):
    meal_categories = {
        "الفطار":0.20,
        "الغداء": 0.40,
        "العشاء": 0.30,
        "السناكس": 0.10
    }
    
    meal_plans = {}
    total_nutrients = {"Protein (g)": 0, "Carbohydrates (g)": 0, "Fat (g)": 0}

    for meal_category, percentage in meal_categories.items():
        calorie_allowance = calorie_intake * percentage
        meal_plan = []
        category_meals = meals_df[meals_df["Category"] == meal_category]

        if protein_range:
            category_meals = category_meals[(category_meals["Protein (g)"] >= protein_range[0]) & (category_meals["Protein (g)"] <= protein_range[1])]
        if carb_range:
            category_meals = category_meals[(category_meals["Carbohydrates (g)"] >= carb_range[0]) & (category_meals["Carbohydrates (g)"] <= carb_range[1])]
        if fat_range:
            category_meals = category_meals[(category_meals["Fat (g)"] >= fat_range[0]) & (category_meals["Fat (g)"] <= fat_range[1])]

        category_meals = category_meals.sample(frac=1)

        for index, row in category_meals.iterrows():
            meal_name = row["Meal Name"]
            meal_calories = row["Calories"]

            if meal_calories <= calorie_allowance:
                meal_plan.append({
                    "Meal": meal_name,
                    "Calories": meal_calories,
                    "Ingredients": row["Ingredients"],
                    "Weight (g)": row["Weight (g)"],
                    "Protein (g)": row["Protein (g)"],
                    "Carbohydrates (g)": row["Carbohydrates (g)"],
                    "Fat (g)": row["Fat (g)"],
                    "Category": row["Category"],
                    "Meal Type" : row["Meal Type"]
                })
                calorie_allowance -= meal_calories

                # Add the nutrients of the meal to the total nutrients
                total_nutrients["Protein (g)"] += row["Protein (g)"]
                total_nutrients["Carbohydrates (g)"] += row["Carbohydrates (g)"]
                total_nutrients["Fat (g)"] += row["Fat (g)"]

        meal_plans[meal_category] = meal_plan

    # Check if the total nutrient intake is within the specified ranges
    if protein_range and not (protein_range[0] <= total_nutrients["Protein (g)"] <= protein_range[1]):
        st.warning("Total protein intake is out of the specified range!")
    if carb_range and not (carb_range[0] <= total_nutrients["Carbohydrates (g)"] <= carb_range[1]):
        st.warning("Total carbohydrate intake is out of the specified range!")
    if fat_range and not (fat_range[0] <= total_nutrients["Fat (g)"] <= fat_range[1]):
        st.warning("Total fat intake is out of the specified range!")

    return meal_plans


def display_meal_plan(meal_plan):

  total_calories = 0
  for category, meals in meal_plan.items():
    st.write("----")
    st.markdown(f'<h1 style="text-align:center; font-size: 22px; background-color: lightgreen; padding: 10px;">{category}</div>', unsafe_allow_html=True)
    st.write("")
    for meal_info in meals:
      st.markdown(f"<h1 style='text-align: center; font-size: 18px;background-color: lightgray; padding: 7px;'>{meal_info['Meal']}</h1>", unsafe_allow_html=True)
      with st.expander("**تفاصيل الوجبة**"):
          st.write(f"**Calorie**s : {meal_info['Calories']}kcal")
          st.write(f"**Meal type** : {meal_info['Meal Type']}")
          st.write(f"**مكونات الوجبة  (gm)**  : {meal_info['Ingredients']}")
          st.write(f"**وزن الوجبة**  : {meal_info['Weight (g)']}  جرام")
          st.write(f"**البروتين**  : {meal_info['Protein (g)']}  جرام")
          st.write(f"**الكربوهيدرات**  : {meal_info['Carbohydrates (g)']}  جرام")
          st.write(f"**الدهون**  : {meal_info['Fat (g)']}  جرام")
          st.write(f"**نوع الوجبة**  : {meal_info['Category']}")



      total_calories += meal_info['Calories']  # Add calories to total
  st.info(f"Total Calories of day meals : **{total_calories}** kcal")  # Display total calories

# Function to read patient data
def read_patient_data():
    try:
        patient_df = pd.read_csv(DATA_FILE)
        return patient_df
    except FileNotFoundError:
        st.error("Patient data file not found.")
        return None







def user_input_page():
    if "show_second_page" not in st.session_state or not st.session_state.show_second_page:
      st.title("Ai Calorie Calculator and Meal Generator")
    st.markdown(f"<h1 style='text-align: center; font-size: 12px;background-color: lightgreen; padding: 10px;'>Programmed by Afandy  .  Supervised By : Dr Hassan and Dr Gehad</h1>", unsafe_allow_html=True)

    st.warning(f"Choose your weight goal from the side bar befor calculating and *Results*")
    # Title
    st.title("Patient Data")

    # Patient information inputs
    patient_name = st.text_input("Enter patient Name")
    age = st.number_input("Enter patient age", value=30, step=1)
    gender = st.selectbox("Select your gender", options=["Male", "Female", "Other"])

    # Weight and height input
    st.subheader("Weight and Height:")
    weight = st.number_input("Enter your weight (kg)", value=60.0, step=1.0)
    height = st.number_input("Enter your height (cm)", value=150.0, step=1.0)

    # Body composition input
    st.subheader("Body Composition:")
    body_fat_percentage = st.number_input("Enter your body fat percentage (%)", min_value=5.0, max_value=100.0, step=0.1)
    waist_to_hip_ratio = st.number_input("Enter your waist-to-hip ratio", min_value=0.0, step=0.01)
    lean_body_mass = st.number_input("Enter your lean body mass (kg)", min_value=5.0, step=0.1)





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
   

    st.subheader("Select your weight goals:")
    weight_loss = st.checkbox("Weight loss")
    weight_gain = st.checkbox("Weight gain")
    maintenance = st.checkbox("Maintenance" ,value = True)
    rapid_weight_loss = st.checkbox("Rapid Weight Loss")
    st.subheader("Meals macronutritions :")

    goals = []
    if weight_loss:
        goals.append("Weight loss")
        fat_range = st.slider('Fat (g)', min_value=0, max_value=50, value=(0, 35))
        protein_range = st.slider('Protein (g)', min_value=0, max_value=50, value=(0, 75))
        carb_range = st.slider('Carbohydrates (g)', min_value=0, max_value=100, value=(0, 150))

    if weight_gain:
        goals.append("Weight gain")
        fat_range = st.slider('Fat (g)', min_value=0, max_value=50, value=(0, 40))
        protein_range = st.slider('Protein (g)', min_value=0, max_value=200, value=(0, 56))
        carb_range = st.slider('Carbohydrates (g)', min_value=0, max_value=300, value=(0, 300))
    if maintenance:
        goals.append("Maintenance")
        fat_range = st.slider('Fat (g)', min_value=0, max_value=50, value=(0, 15))
        protein_range = st.slider('Protein (g)', min_value=0, max_value=200, value=(0, 30))
        carb_range = st.slider('Carbohydrates (g)', min_value=0, max_value=300, value=(0, 65))

    if rapid_weight_loss:
        goals.append("Rapid Weight Loss")
        fat_range = st.slider('Fat (g)', min_value=0, max_value=50, value=(0, 25))
        protein_range = st.slider('Protein (g)', min_value=0, max_value=200, value=(0, 85))
        carb_range = st.slider('Carbohydrates (g)', min_value=0, max_value=200, value=(0, 150))




    # Calculate calorie intake
    calorie_intake = calculate_calorie_intake(tdee, goals, weight, ideal_weight)

    # Read meals from CSV
    meals_df = pd.read_csv("food.csv", encoding='utf-8-sig')



    # Buttons
    if st.button("Save Patient Data"):
        patient_data = {
            "patient_name": patient_name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "body_fat_percentage": body_fat_percentage,
            "waist_to_hip_ratio": waist_to_hip_ratio,
            "lean_body_mass": lean_body_mass
        }
        # save_patient_data(patient_data)
        st.success("Patient data saved successfully.")
    
    # Display calculated metrics
        st.header("Results")
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
        st.write("----")
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
    st.write("----")    
    st.success(
            f"Recommended Daily Calorie Intake *According to your weight plan*: {calorie_intake:.2f} kcal/day")

    # Define the range for each nutrient

    





    
    # Display Meals
    if st.button("Generate meals"):
        meal_plan = generate_meal_plan(calorie_intake, meals_df, protein_range, carb_range, fat_range)
        display_meal_plan(meal_plan)







    details = st.button("Generate Meals for Week")
    if details:
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 22px;background-color: #FFB6C1;'>اليوم الأول</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df, protein_range, carb_range, fat_range)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 22px;background-color: #FFB6C1;'>اليوم الثاني</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df, protein_range, carb_range, fat_range)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 22px;background-color: #FFB6C1;'>اليوم الثالث</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df, protein_range, carb_range, fat_range)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 22px;background-color: #FFB6C1;'>اليوم الرابع</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df, protein_range, carb_range, fat_range)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 22px;background-color: #FFB6C1;'>اليوم الخامس</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df, protein_range, carb_range, fat_range)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 22px;background-color: #FFB6C1;'>اليوم السادس</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df, protein_range, carb_range, fat_range)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 22px;background-color: #FFB6C1;'>اليوم السابع</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df, protein_range, carb_range, fat_range)
        display_meal_plan(meal_plan)








if __name__ == "__main__":
    user_input_page()
