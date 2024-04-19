import streamlit as st
import pandas as pd
import csv
import os
import datetime


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


def get_patient_weight_data(patient_data, patient_name):
    # Placeholder implementation - Replace with actual data retrieval logic
    # This function should retrieve weight data for the specified patient
    if patient_data:
        return patient_data.get('weight', {})
    else:
        return {}



def display_patient_data_page(patient_data):
    st.title("Patient Data")
    st.write(f"Patient Name: {patient_data['patient_name']}")
    st.write(f"Age: {patient_data['age']}")
    st.write(f"Gender: {patient_data['gender']}")
    st.write(f"Weight (kg): {patient_data['weight']}")
    st.write(f"Height (cm): {patient_data['height']}")
    st.write(f"Body Fat Percentage (%): {patient_data['body_fat_percentage']}")
    st.write(f"Waist-to-Hip Ratio: {patient_data['waist_to_hip_ratio']}")
    st.write(f"Lean Body Mass (kg): {patient_data['lean_body_mass']}")


    return pdf_path

# Define function to read meals and their calorie counts from CSV
def read_meals_from_csv(csv_file):
  meals_df = pd.read_csv("food.csv", encoding='utf-8-sig')
  return meals_df
# Save the meal plan as an image
# Function to save meal plan as an image
def save_meal_plan_as_image(meal_plan):
    # Create a blank image with white background
    image = Image.new('RGB', (800, 600), 'white')
    draw = ImageDraw.Draw(image)

    # Set font and size
    font = ImageFont.truetype('arial.ttf', 24)

    # Draw meal plan text
    y = 50
    for category, meals in meal_plan.items():
        draw.text((50, y), category, fill='black', font=font)
        y += 50
        for meal_info in meals:
            draw.text((100, y), f"{meal_info['Meal']} - Calories: {meal_info['Calories']}", fill='black', font=font)
            y += 30

    # Save the image
    image.save('meal_plan.png')

def generate_meal_plan(calorie_intake, meals_df):
    # Define the calorie distribution for each meal category based on the user's input calorie intake
    meal_categories = {
        "الفطار": 0.25,
        "الغداء": 0.40,
        "العشاء": 0.25,
        "سناكس": 0.10
    }

    # Calculate the calorie allowance for each meal category based on the recommended intake
    calorie_allowance = {category: calorie_intake * percentage for category, percentage in meal_categories.items()}

    # Initialize empty lists to store selected meals for each category
    meal_plan = {category: [] for category in meal_categories}

    # Shuffle the DataFrame to get random meals
    shuffled_meals = meals_df.sample(frac=1).reset_index(drop=True)


    for index, row in shuffled_meals.iterrows():
        meal_name = row["Meal Name"]
        meal_calories = row["Calories"]
        
        # Check if the meal fits into any of the categories based on remaining calorie allowance
        for category, allowance in calorie_allowance.items():
            if meal_calories <= allowance:
                # Add the meal to the corresponding category
                meal_plan[category].append({
                    "Meal": meal_name,
                    "Calories": meal_calories,
                    "Ingredients": row["Ingredients"],
                    "Weight (g)": row["Weight (g)"],
                    "Protein (g)": row["Protein (g)"],
                    "Carbohydrates (g)": row["Carbohydrates (g)"],
                    "Fat (g)": row["Fat (g)"],
                    "Meal Type": row["Meal Type"]
                })
                # Deduct the calories of the meal from the remaining allowance for the category
                calorie_allowance[category] -= meal_calories
                break  # Move to the next meal once added to a category

    return meal_plan



def display_meal_plan(meal_plan):
  total_calories = 0
  for category, meals in meal_plan.items():
    st.write("----")
    st.markdown(f'<div style="text-align:center; font-size: 24px; background-color: lightblue; padding: 10px;">{category}</div>', unsafe_allow_html=True)
    st.write("")
    for meal_info in meals:
      st.markdown(f"<h1 style='text-align: center; font-size: 20px;background-color: lightblue; padding: 10px;'>{meal_info['Meal']}</h1>", unsafe_allow_html=True)
      with st.expander("**تفاصيل الوجبة**", expanded=True):
          st.write(f"Calories : {meal_info['Calories']}kcal")
          st.write(f"**مكونات الوجبة  (gm)**  : {meal_info['Ingredients']}")
          st.write(f"**وزن الوجبة**  : {meal_info['Weight (g)']}  جرام")
          st.write(f"**البروتين**  : {meal_info['Protein (g)']}  جرام")
          st.write(f"**الكربوهيدرات**  : {meal_info['Carbohydrates (g)']}  جرام")
          st.write(f"**الدهون**  : {meal_info['Fat (g)']}  جرام")



      total_calories += meal_info['Calories']  # Add calories to total
  st.info(f"Total Calories of day meals : **{total_calories}** kcal")  # Display total calories





def user_input_page():
    st.title("Ai Calorie Calculator and Meal Generator")
    st.markdown(f"<h1 style='text-align: center; font-size: 12px;background-color: lightgreen; padding: 10px;'>Programmed by Afandy  .  Supervised By : Dr Hassan and Dr Gehad</h1>", unsafe_allow_html=True)

    st.warning(f"Choose your weight goal from the side bar befor calculating and *Results*")
    # Title
    st.title("Patient Data")

    # Patient information inputs
    patient_name = st.text_input("Enter patient Name")
    age = st.number_input("Enter patient age", min_value=1, max_value=150, step=1)
    gender = st.selectbox("Select your gender", options=["Male", "Female", "Other"])

    # Weight and height input
    st.subheader("Weight and Height:")
    weight = st.number_input("Enter your weight (kg)", min_value=10.0, step=1.0)
    height = st.number_input("Enter your height (cm)", min_value=50.0, step=1.0)

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
    st.sidebar.subheader("Select your dietary goals:")
    weight_loss = st.sidebar.checkbox("Weight loss")
    weight_gain = st.sidebar.checkbox("Weight gain")
    maintenance = st.sidebar.checkbox("Maintenance")
    fitness = st.sidebar.checkbox("Fitness", True)
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
    if st.button("Results"):
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



    
    # Display Meals
    if st.checkbox("Generate Meals for one day"):  
        meal_plan = generate_meal_plan(calorie_intake, meals_df)
        display_meal_plan(meal_plan)

    details = st.checkbox("Generate Meals for Week")
    if details:
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 20px;background-color: #FFB6C1;'>اليوم الأول</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 20px;background-color: #FFB6C1;'>اليوم الثاني</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 20px;background-color: #FFB6C1;'>اليوم الثالث</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 20px;background-color: #FFB6C1;'>اليوم الرابع</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 20px;background-color: #FFB6C1;'>اليوم الخامس</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 20px;background-color: #FFB6C1;'>اليوم السادس</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df)
        display_meal_plan(meal_plan)
        st.markdown(f"<h1 style='text-align: center;font-family: tahoma; font-size: 20px;background-color: #FFB6C1;'>اليوم السابع</h1>", unsafe_allow_html=True)
        meal_plan = generate_meal_plan(calorie_intake, meals_df)
        display_meal_plan(meal_plan)


if __name__ == "__main__":
    user_input_page()
