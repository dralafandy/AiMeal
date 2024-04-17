import streamlit as st
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
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


# Function to search for a patient by name
def search_patient_by_name(patient_name):
    with open(DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["patient_name"] == patient_name:
                return row
    return None

# Function to update patient data
def update_patient_data(patient_name, updated_data):
    rows = []
    with open(DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["patient_name"] == patient_name:
                row.update(updated_data)
            rows.append(row)
    
    with open(DATA_FILE, mode='w', newline='') as file:
        fieldnames = rows[0].keys() if rows else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Function to display patient metrics chart
def display_patient_metrics_chart():
    st.title("Patient Metrics Chart")
    patient_data = {"weight": [], "body_fat_percentage": [], "lean_body_mass": [], "waist_to_hip_ratio": []}
    with open(DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date_time = datetime.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
            for metric in patient_data:
                  patient_data[metric].append(float(row[metric.lower().replace(' ', '_')]))

    # Plot patient metrics for each patient
    if patient_data:
        fig, ax = plt.subplots()
        for metric, values in patient_data.items():
            ax.plot(patient_data["weight"], values, label=metric)
        ax.set_xlabel("Weight (kg)")
        ax.set_ylabel("Metrics")
        ax.set_title("Patient Metrics Progression")
        ax.legend()
        st.pyplot(fig)

# Function to display weight progression chart
def display_weight_progression_chart():
    st.title("Weight Progression Chart")
    weight_data = {}
    with open(DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date_time = datetime.datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
            if row["patient_name"] not in weight_data:
                weight_data[row["patient_name"]] = {"datetimes": [], "weights": []}
            weight_data[row["patient_name"]]["datetimes"].append(row["datetime"])
            weight_data[row["patient_name"]]["weights"].append(float(row["weight"]))

    # Plot weight progression for each patient
    if weight_data:
        fig, ax = plt.subplots()
        for patient_name, data in weight_data.items():
            ax.plot(data["datetimes"], data["weights"], label=patient_name)
        ax.set_xlabel("Date and Time")
        ax.set_ylabel("Weight (kg)")
        ax.set_title("Weight Progression")
        ax.legend()
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        st.pyplot(fig)




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

# Function to display all patient data
def display_all_patient_data():
    st.title("All Patient Data")
    patient_weight_data = {}
    with open(DATA_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            st.write("Patient Name:", row["patient_name"])
            st.write("Age:", row["age"])
            st.write("Gender:", row["gender"])
            st.write("Weight (kg):", row["weight"])
            st.write("Height (cm):", row["height"])
            st.write("Body Fat Percentage (%):", row["body_fat_percentage"])
            st.write("Waist-to-Hip Ratio:", row["waist_to_hip_ratio"])
            st.write("Lean Body Mass (kg):", row["lean_body_mass"])
            st.write("")

            # Store weight data for each patient
            patient_weight_data[row["patient_name"]] = float(row["weight"])

    # Plot weight progression for each patient
    if patient_weight_data:
        st.subheader("Weight Progression")
        fig, ax = plt.subplots()
        ax.bar(patient_weight_data.keys(), patient_weight_data.values())
        ax.set_xlabel("Patient Name")
        ax.set_ylabel("Weight (kg)")
        ax.set_title("Weight Progression for Each Patient")
        st.pyplot(fig)



# Define function to read meals and their calorie counts from CSV
def read_meals_from_csv(csv_file):
  meals_df = pd.read_csv("food.csv", encoding='utf-8-sig')
  return meals_df


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


def generate_multi_day_meal_plan(calorie_intake, meals_df, num_days):
    # Define the calorie distribution for each meal category
    meal_categories = {
        "الفطار": 0.25,
        "الغداء": 0.40,
        "العشاء": 0.25,
        "سناكس": 0.10
    }

    # Initialize a dictionary to store the meal plan for each day
    multi_day_meal_plan = {day: None for day in range(1, num_days + 1)}

    for day in range(1, num_days + 1):
        # Calculate the calorie allowance for each meal category for the day
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

        # Store the meal plan for the day
        multi_day_meal_plan[day] = meal_plan

    return multi_day_meal_plan





def display_meal_plan(meal_plan):
  st.subheader("Ai Meal Plan:")
  total_calories = 0
  for category, meals in meal_plan.items():
    st.write("----")
    st.markdown(f"<h1 style='color: blue; text-align: center;'>{category}</h1>", unsafe_allow_html=True)
    for meal_info in meals:
      st.markdown(f"<h1 style='text-align: center; font-size: 20px;'>{meal_info['Meal']}</h1>", unsafe_allow_html=True)
      with st.expander("**تفاصيل الوجبة**"):
          st.write(f"Calories : {meal_info['Calories']}kcal")
          st.write(f"**مكونات الوجبة  (gm)**  : {meal_info['Ingredients']}")
          st.write(f"**وزن الوجبة**  : {meal_info['Weight (g)']}  جرام")
          st.write(f"**البروتين**  : {meal_info['Protein (g)']}  جرام")
          st.write(f"**الكربوهيدرات**  : {meal_info['Carbohydrates (g)']}  جرام")
          st.write(f"**الدهون**  : {meal_info['Fat (g)']}  جرام")



      total_calories += meal_info['Calories']  # Add calories to total
  st.info(f"Total Calories of day meals : **{total_calories}** kcal")  # Display total calories






      
      

def user_input_page():
  st.title("AI Calorie Calculator")

  # Sidebar for additional options
  st.sidebar.title("البيانات")

  # Age input
  patient_name = st.sidebar.text_input("Enter patient Name")

  # Age input
  age = st.sidebar.number_input("Enter patient age",
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

  # Sidebar buttons
  if st.sidebar.button("Save Patient Data"):
      # Assuming you have patient data in the format of a dictionary
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

      # Save patient data
      save_patient_data(patient_data)
      st.sidebar.success("Patient data saved successfully.")

  if st.sidebar.button("Search Patient"):
      # Search for a patient by name
      search_result = search_patient_by_name(patient_name)
      if search_result:
          display_patient_data_page(search_result)  # Display patient data page
      else:
          st.sidebar.write("Patient not found.")

  if st.sidebar.button("Update Patient Data"):
      updated_age = st.sidebar.number_input("Enter updated age", value=age)
      # Update patient data
      update_patient_data(patient_name, {"age": updated_age})
      st.sidebar.success("Patient data updated successfully.")

  # Button to display all patient data
  if st.sidebar.button("Display All Patient Data"):
      display_all_patient_data()
 
  # Button to display weight progression chart
  if st.sidebar.button("Display Weight Progression Chart"):
      display_weight_progression_chart()

  # Button to display patient metrics chart
  if st.sidebar.button("Display Patient Metrics Chart"):
      display_patient_metrics_chart()








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


  meal_plan = generate_meal_plan(calorie_intake, meals_df)
  display_meal_plan(meal_plan)


if __name__ == "__main__":
  user_input_page()
