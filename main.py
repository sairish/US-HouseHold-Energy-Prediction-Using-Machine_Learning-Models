# pip install -r requirements.txt
import pickle
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Load the trained model and preprocessor
multioutput_regressor_rf = pickle.load(open(r'C:\Users\Acer\Desktop\Rishi_MLProject\Energy_Consumption_Model_RF.pkl','rb'))
preprocessor = pickle.load(open(r'C:\Users\Acer\Desktop\Rishi_MLProject\preprocessor.pkl','rb'))

# Prediction function
def prediction(Month, kwh_total_sqft, electricity_accounts, renter_occupied_housing_percentage, renter_occupied_housing_units, occupied_units_percentage, average_building_age, average_housesize, average_stories, total_population, zero_kwh_accounts):
    input_data = (Month, kwh_total_sqft, electricity_accounts, renter_occupied_housing_percentage, renter_occupied_housing_units, occupied_units_percentage, 
                  average_building_age, average_housesize, average_stories, total_population, zero_kwh_accounts)
    col_names = ['Month', 'KWH TOTAL SQFT', 'ELECTRICITY ACCOUNTS', 'RENTER-OCCUPIED HOUSING PERCENTAGE', 'RENTER-OCCUPIED HOUSING UNITS', 'OCCUPIED UNITS PERCENTAGE',
                 'AVERAGE BUILDING AGE', 'AVERAGE HOUSESIZE', 'AVERAGE STORIES', 'TOTAL POPULATION', 'ZERO KWH ACCOUNTS']
    features = pd.DataFrame([input_data], columns=col_names)
    transform_features = preprocessor.transform(features)
    predicted_val = multioutput_regressor_rf.predict(transform_features).reshape(-1, 1)
    return predicted_val

# Sidebar with page options
with st.sidebar:
    selected = option_menu("Household Energy Prediction System",
                           ["Energy prediction based on area sqft", "Energy prediction Trend"])

# List of months
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# First page - Energy prediction based on area sqft
if selected == "Energy prediction based on area sqft":
    st.title("Energy prediction based on area(sqft)")

    # Columns for input fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Month = st.selectbox('Select a month:', months)
        kwh_total_sqft = st.number_input('KWH TOTAL SQFT',min_value=100, step=500, value=st.session_state.get('kwh_total_sqft', 100))
        electricity_accounts = st.number_input('ELECTRICITY ACCOUNTS', min_value=0, step=1, value=st.session_state.get('electricity_accounts', 0))
        renter_occupied_housing_percentage = st.number_input('OCCUPIED HOUSING PERCENTAGE', min_value=0.0, max_value=1.0, step=0.1, value=st.session_state.get('renter_occupied_housing_percentage', 0.0))
        
    with col2:
        renter_occupied_housing_units = st.number_input('OCCUPIED HOUSING UNITS',min_value=0, step=1, value=st.session_state.get('renter_occupied_housing_units', 0))
        occupied_units_percentage = st.number_input('OCCUPIED UNITS PERCENTAGE', min_value=0.0, max_value=1.0, step=0.1, value=st.session_state.get('occupied_units_percentage', 0.0))
        average_building_age = st.number_input('AVERAGE BUILDING AGE',min_value=0, step=5, value=st.session_state.get('average_building_age', 1))
        average_housesize = st.number_input('AVERAGE HOUSESIZE',min_value=0, step=1, value=st.session_state.get('average_housesize',0))

    with col3:
        average_stories = st.number_input('AVERAGE STORIES', min_value=1, max_value=150, step=2, value=st.session_state.get('average_stories', 1))
        total_population = st.number_input('TOTAL POPULATION',min_value=0, step=10, value=st.session_state.get('total_population', 0))
        zero_kwh_accounts = st.number_input('ZERO KWH ACCOUNTS', min_value=0, step=1, value=st.session_state.get('zero_kwh_accounts', 0))

    # Save session data when button is clicked
    if st.button('Show Household Energy Consumption'):
        # Store the inputs into session_state
        st.session_state.kwh_total_sqft = kwh_total_sqft
        st.session_state.electricity_accounts = electricity_accounts
        st.session_state.renter_occupied_housing_percentage = renter_occupied_housing_percentage
        st.session_state.renter_occupied_housing_units = renter_occupied_housing_units
        st.session_state.occupied_units_percentage = occupied_units_percentage
        st.session_state.average_building_age = average_building_age
        st.session_state.average_housesize = average_housesize
        st.session_state.average_stories = average_stories
        st.session_state.total_population = total_population
        st.session_state.zero_kwh_accounts = zero_kwh_accounts

        # Prediction
        input_list = (Month, kwh_total_sqft, electricity_accounts, renter_occupied_housing_percentage, renter_occupied_housing_units, occupied_units_percentage,
                      average_building_age, average_housesize, average_stories, total_population, zero_kwh_accounts)
        energy_pred = prediction(*input_list)
        TOTAL_KWH = energy_pred[0][0]
        TOTAL_THERMS = energy_pred[1][0]
        MONTHLY_KWH = energy_pred[2][0]
        MONTHLY_THERMS = energy_pred[3][0]

        # Store output in session_state
        st.session_state.TOTAL_KWH = TOTAL_KWH
        st.session_state.TOTAL_THERMS = TOTAL_THERMS
        st.session_state.MONTHLY_KWH = MONTHLY_KWH
        st.session_state.MONTHLY_THERMS = MONTHLY_THERMS
        

    # Show previously stored session data on the first page if available
    if 'TOTAL_KWH' in st.session_state:
        TOTAL_KWH = st.session_state.TOTAL_KWH
        TOTAL_THERMS = st.session_state.TOTAL_THERMS
        MONTHLY_KWH = st.session_state.MONTHLY_KWH
        MONTHLY_THERMS = st.session_state.MONTHLY_THERMS
        Annual_output = f"ANNUAL_KWH: {TOTAL_KWH:.2f} & ANNUAL_THERMS: {TOTAL_THERMS:.2f}"
        Monthly_output = f"{Month}: MONTHLY_KWH: {MONTHLY_KWH:.2f} & MONTHLY_THERMS: {MONTHLY_THERMS:.2f}"
        st.success(Annual_output)
        st.success(Monthly_output)

    if st.button('Reset'):
        st.session_state.clear()  # This will clear all session variables

################----------------------######################################---------------------------------########################################################
################----------------------######################################---------------------------------########################################################
################----------------------######################################---------------------------------########################################################

# Second page - Energy prediction Trend
if selected == "Energy prediction Trend":
    st.title("Energy prediction Trend")

    # Ensure that session state is available
    if 'kwh_total_sqft' in st.session_state:
        kwh_total_sqft = st.session_state.kwh_total_sqft
        electricity_accounts = st.session_state.electricity_accounts
        renter_occupied_housing_percentage = st.session_state.renter_occupied_housing_percentage
        renter_occupied_housing_units = st.session_state.renter_occupied_housing_units
        occupied_units_percentage = st.session_state.occupied_units_percentage
        average_building_age = st.session_state.average_building_age
        average_housesize = st.session_state.average_housesize
        average_stories = st.session_state.average_stories
        total_population = st.session_state.total_population
        zero_kwh_accounts = st.session_state.zero_kwh_accounts

        # Initialize lists to store monthly predictions
        months_list = []
        total_kwh_list = []
        total_therms_list = []
        monthly_kwh_list = []
        monthly_therms_list = []

        # Collect monthly predictions
        for Month in months:
            input_list = (Month, kwh_total_sqft, electricity_accounts, renter_occupied_housing_percentage, renter_occupied_housing_units, occupied_units_percentage,
                          average_building_age, average_housesize, average_stories, total_population, zero_kwh_accounts)
            energy_pred = prediction(*input_list)
            TOTAL_KWH = energy_pred[0][0]
            TOTAL_THERMS = energy_pred[1][0]
            MONTHLY_KWH = energy_pred[2][0]
            MONTHLY_THERMS = energy_pred[3][0]
            
            # Append results to lists
            months_list.append(Month)
            total_kwh_list.append(TOTAL_KWH)
            total_therms_list.append(TOTAL_THERMS)
            monthly_kwh_list.append(MONTHLY_KWH)
            monthly_therms_list.append(MONTHLY_THERMS)

        # Create a DataFrame for the trend
        trend_df = pd.DataFrame({
            'Month': months_list,
            'TOTAL_KWH': total_kwh_list,
            'TOTAL_THERMS': total_therms_list,
            'MONTHLY_KWH': monthly_kwh_list,
            'MONTHLY_THERMS': monthly_therms_list
        })

        # Make sure the months are in correct order
        trend_df['Month'] = pd.Categorical(trend_df['Month'], categories=months, ordered=True)
        trend_df = trend_df.sort_values('Month')

        # Plot bar charts for each category

        st.subheader("Monthly KWH Trend")
        st.bar_chart(trend_df.set_index('Month')['MONTHLY_KWH'])

        st.subheader("Monthly Therms Trend")
        st.bar_chart(trend_df.set_index('Month')['MONTHLY_THERMS'])

        # Display trend data
        st.subheader("Monthly Trend Data Table")
        st.dataframe(trend_df)


        if st.button('Reset'):
            st.session_state.clear()  # This will clear all session variables

# Run below line in terminal to execute code
# streamlit run c:/Users/Acer/Desktop/Rishi_MLProject/main.py
# Use Ctrl + C to stop executing 