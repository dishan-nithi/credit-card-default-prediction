import streamlit as st
import streamlit_authenticator as stauth
import joblib
import pandas as pd
import altair as alt
from streamlit_extras.switch_page_button import switch_page
import shap
import matplotlib.pyplot as plt
import numpy as np
import math

def main():
    cols = st.columns(5)
    
# the 3rd column
    st.title("Credit Card Default Predictor")

    with open('uploads/status.txt','r') as f:
        status_file=f.read()
    
    with cols[4]:
            if st.button('Go Back'):
                st.switch_page("app.py")        
        
    if 'True' in status_file:
        model = joblib.load('models/final_model.pkl')
        data = pd.read_csv('uploads/final_test_df.csv')
        data_sample=data.drop(columns=['ACC_NO'])
        
        account_number = st.text_input("Enter Account Number", "")

        if account_number:
            try:
                data2=data[data['ACC_NO']==int(account_number)]
                data2=data2.drop(columns=['ACC_NO'])

                explainer = shap.TreeExplainer(model, data=data_sample.iloc[0:5],model_output='probability')
                
                shap_values = explainer(data2)
                
                fig = plt.figure(figsize=(10, 6))
                shap.plots.waterfall(shap_values[0], show=False)
                st.pyplot(fig)
                
                probability_percentage = model.predict_proba(data2)[0,1] * 100
                st.write(f"### Default Probability: **{probability_percentage:.2f}%**")
                
                
            except ValueError:
                st.write("Please enter a valid account number")
    
    else:
        st.write('Invalid Schema. Please try again.')    
    
if __name__ == "__main__":
    main()