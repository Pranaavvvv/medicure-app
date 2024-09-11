import streamlit as st
import pandas as pd

# Load the data from the CSV file
file_path = 'Medicine_Details.csv'
data = pd.read_csv(file_path)

# Remove duplicate rows
data.drop_duplicates(inplace=True)

correction_dict = {
    'Dibetis': 'Diabetes',
    'Hypertention': 'Hypertension',
    # Add more corrections as needed
}

def correct_grammar(text):
    for wrong, correct in correction_dict.items():
        text = text.replace(wrong, correct)
    return text

data['Uses'] = data['Uses'].apply(correct_grammar)

# Extract unique diseases from the 'Uses' column
diseases = set()
for uses in data['Uses'].dropna():
    for disease in uses.split(','):
        disease = disease.strip().replace("Treatment of ", "")
        diseases.add(disease)

# Convert the set to a sorted list for the dropdown
disease_list = sorted(diseases)

# Function to build the recommendation system
def recommend_medicine(disease):
    # Filter the dataset for the given disease
    recommended_medicines = data[data['Uses'].str.contains(disease, case=False, na=False)]
    
    if recommended_medicines.empty:
        return f"No medicines found for the disease: {disease}"
    
    return recommended_medicines[['Medicine Name', 'Composition', 'Uses', 'Side_effects', 'Manufacturer', 'Excellent Review %', 'Average Review %', 'Poor Review %']]

# Streamlit app
st.title("Medicine Recommendation System")

# Dropdown for selecting disease
selected_disease = st.selectbox("Select a disease:", [""] + disease_list)

# Display recommendations
if selected_disease:
    recommendations = recommend_medicine(selected_disease)
    if isinstance(recommendations, str):
        st.write(recommendations)
    else:
        st.write("### Recommended Medicines")
        st.dataframe(recommendations)
