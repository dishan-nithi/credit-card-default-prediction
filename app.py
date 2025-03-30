#from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import numpy as np
import pandas as pd
from default_predictor.pipeline.prediction import PredictionPipeline
from default_predictor.utils.common import check_schema, read_yaml, clean_df
from default_predictor.constants import SCHEMA_FILE_PATH
from default_predictor.components.page_authenticator import PageAuthenticator
from pathlib import Path
import streamlit as st
import pickle
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page
import mysql.connector


names = ['Dishan N','Dishan2']
usernams = ['Dishan','Dishan2']
Passwords = ['zxc123','zxc1234']
hashed_passwords=["$2b$12$H6R53pkIR49nlm7/eWVwlO7jyHTQzkcN9KVgL7idQbN/0cC7j6FYO","$2b$12$9eQurRnALuG.7JPeK31fgeWN6hpKFlHz7ZFBdDGeqJ.0Odb.QvDVu"]


    
authenticator = stauth.Authenticate(usernams, usernams,  hashed_passwords, "streamlit_app", "cookies",cookie_expiry_days=1)


def main():
    cols = st.columns(5)
    

# the 3rd column
    with cols [0]:
        toggle_dark = st.toggle("Dark Layout", value=True)
        if st.get_option("theme.base") == "light" and toggle_dark:
            st._config.set_option("theme.base", "dark")  # type: ignore # noqa: SLF001
            st.rerun()
        elif st.get_option("theme.base") == "dark" and not toggle_dark:
            st._config.set_option("theme.base", "light")  # type: ignore # noqa: SLF001
            st.rerun()
    with cols[4]:
        authenticator.logout("Logout", "main")
    st.title("Credit Card Default Predictor")
    

        
    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file here", type="csv", accept_multiple_files=False)

    #sidebar
    #authenticator.logout('Logout','main')
    
    # Placeholder for status messages
    status_placeholder = st.empty()

    if uploaded_file is not None:
        # Check file type
        if uploaded_file.name.endswith('.csv'):
            # Display uploaded file name
            st.success(f"File '{uploaded_file.name}' uploaded successfully.")
            
            directory_path = r"uploads" 
            file_dir =Path(os.path.join(directory_path,uploaded_file.name))

            # Button to send the file
            if st.button("Send File"):
                # Simulate sending the file
                status_placeholder.success(f"File '{uploaded_file.name}' sent successfully!")
                
                for filename in os.listdir(directory_path):
                    
                    os.chmod(directory_path, 0o666)
                    # Check if the file ends with .csv
                    if filename.endswith('.csv'):
                        
                        file_path = os.path.join(directory_path, filename)
                        os.chmod(file_path, 0o666)
                        os.remove(file_path)
                        print(f"Deleted {file_path}")
                
                #Saving inside the folder
                with open(file_dir,'wb') as f:
                    f.write(uploaded_file.getbuffer())
                    
                #Checking schema
                data = clean_df(file_dir)
                data.to_csv(file_dir, index=False)
                all_columns = list(data.columns)
                all_schema = read_yaml(SCHEMA_FILE_PATH).COLUMNS
                check_schema(path_of_csv=file_dir, schema=all_schema,path_of_status_file=Path('uploads/status.txt'))
                
                with open('uploads/status.txt','r') as f:
                    status_file=f.read()
                
                
                if 'True' in status_file:
                    switch_page("result_page")
                else:
                    st.write('Invalid Schema. Please try again.')
                #nav_page('result_page')
                #


                
                
        else:
            status_placeholder.error("Error: Please upload a valid CSV file.")
    else:
        st.info("Please upload a file to proceed.")
        
        
        



name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("The user credentials are incorrect")
    
if authentication_status == None:
    st.warning("Please enter your credentials")
    
if authentication_status == True:

    if __name__ == "__main__":
        main()
