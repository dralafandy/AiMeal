import streamlit as st
import pandas as pd

# Define the file path for storing patient data
DATA_FILE = "patient_data.csv"

# Function to read patient data
def read_patient_data():
    try:
        patient_df = pd.read_csv(DATA_FILE)
        return patient_df
    except FileNotFoundError:
        st.error("Patient data file not found.")
        return None

def calculate_change(df, column):
    return df[column].diff().fillna(0)
def patient_data_page():
    st.title("Patient Data Analysis")

    # Read patient data
    patient_df = read_patient_data()

    if patient_df is not None:
        # Display dropdown menu with patient names
        selected_patient = st.selectbox("Select a patient", patient_df["patient_name"].unique())

        # Filter patient data based on selected patient
        filtered_patient_data = patient_df[patient_df["patient_name"] == selected_patient]

        # Display patient data
        st.write("### Patient Data Overview")
        st.dataframe(filtered_patient_data)

        # Display weight progression chart
        st.write("### Weight Progression Over Time")
        weight_chart_data = filtered_patient_data.set_index("datetime")[["weight", "body_fat_percentage", "lean_body_mass"]]
        st.line_chart(weight_chart_data, use_container_width=True)

        # Calculate changes in weight, body fat percentage, and lean body mass
        filtered_patient_data["weight_change"] = calculate_change(filtered_patient_data, "weight")
        filtered_patient_data["body_fat_percentage_change"] = calculate_change(filtered_patient_data, "body_fat_percentage")
        filtered_patient_data["lean_body_mass_change"] = calculate_change(filtered_patient_data, "lean_body_mass")

        
        # Display weight, body fat percentage, and lean body mass progression chart
        st.write("### Changes in Weight, Body Fat Percentage, and Lean Body Mass Over Time")
        chart_data = filtered_patient_data.set_index("datetime")[["weight_change", "body_fat_percentage_change", "lean_body_mass_change"]]
        st.line_chart(chart_data, use_container_width=True)

        # Display change in weight
        st.write("### Change in Weight Over Time")
        weight_change_data = filtered_patient_data.set_index("datetime")["weight_change"]
        st.line_chart(weight_change_data, use_container_width=True)

        # Display the most recent change in weight in a box
        latest_weight_change = filtered_patient_data["weight_change"].iloc[-1]
        st.info(f"Latest change in weight: {latest_weight_change:.2f} kg")


if __name__ == "__main__":
    patient_data_page()
