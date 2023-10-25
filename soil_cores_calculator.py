
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Define the polynomial function to predict multiplier (a) based on CV
def polynomial_function(cv):
    return 4.80 * cv ** 2 - 86.97 * cv + 1782.71

# Define the final power function to predict the number of soil cores based on Error and CV
def final_power_function(error, cv):
    a = polynomial_function(cv)
    b = -1.98
    return max(a * (error ** b), 0)

# Initialize session state for storing calculations
if 'calc_data' not in st.session_state:
    st.session_state.calc_data = []

# Layout and Components
st.title("Soil Cores Calculator")
st.subheader("Author: Trung Nguyen")
st.write(f"Based on Gilbert 1987 from Fertcare Sampling Guide 2019")

# Mode selection
mode = st.radio("Select Calculation Mode:", ["Calculate Number of Soil Cores", "Calculate Error (%)"])

# CV slider
cv = st.slider("Coefficient of Variation (CV %)", min_value=3, max_value=90, value=30, step=1)

# Error or Soil Cores slider based on mode
if mode == "Calculate Number of Soil Cores":
    error = st.slider("Error (%)", min_value=5, max_value=50, value=10, step=1)
    st.write(f"Selected Error: {error}%")
else:
    soil_cores = st.slider("Number of Soil Cores", min_value=0, max_value=1000, value=20, step=1)
    st.write(f"Selected Number of Soil Cores: {soil_cores}")

# Calculate button
if st.button("Calculate"):
    if mode == "Calculate Number of Soil Cores":
        calculated_cores = final_power_function(error, cv)
        st.session_state.calc_data.append(("Soil Cores", error, cv, calculated_cores))
        st.write(f'<p style="color:green;font-weight:bold;">Calculated Number of Soil Cores: {calculated_cores:.0f}%</p>',unsafe_allow_html=True)
    else:
        # Calculate Error by inverting the power function
        a = polynomial_function(cv)
        calculated_error = (soil_cores / a) ** (1 / -1.98)
        st.session_state.calc_data.append(("Error", calculated_error, cv, soil_cores))
        # st.write(f"Calculated Error: {calculated_error:.2f}%")
        st.markdown(f'<p style="color:blue;font-weight:bold;">Calculated Error: {calculated_error:.2f}%</p>', unsafe_allow_html=True)

# Clear Data button
if st.button("Clear Data"):
    st.session_state.calc_data = []
    st.write("Cleared all data.")

# Plot
if st.session_state.calc_data:
    fig, ax = plt.subplots()
    for calc_type, x_val, cv_val, y_val in st.session_state.calc_data:
        y_val = round(y_val)
        if calc_type == "Soil Cores":
            ax.scatter(x_val, y_val, label=f"Error: {x_val}%, CV: {cv_val}%, N: {y_val}", marker='o')
        else:
            ax.scatter(x_val, y_val, label=f"Error: {x_val:.2f}%, CV: {cv_val}%, N: {y_val}", marker='x')
    ax.set_xlabel("Error (%)")
    ax.set_ylabel("Number of Soil Cores")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
