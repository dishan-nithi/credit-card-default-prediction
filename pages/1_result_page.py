import streamlit as st
import pickle
import streamlit_authenticator as stauth
import joblib
import pandas as pd
import altair as alt
from streamlit_extras.switch_page_button import switch_page
#
def main():
    cols = st.columns(5)


# the 3rd column
    st.title("Credit Card Default Predictor")
    with open('uploads/status.txt','r') as f:
        status_file=f.read()


    if 'True' in status_file:
        
        model = joblib.load('models/final_model.pkl')
        data = pd.read_csv('uploads/final_test_df.csv')
        acc_no=data['ACC_NO']
        data=data.drop(columns=['ACC_NO'])
        
        data['PREDICTION'] = model.predict(data)
        data.insert(0,'ACC_NO',acc_no)
        data.to_csv('uploads/predicted_df.csv', index=False)
        csv = data.to_csv().encode('utf-8')
        
        st.write("Click the button to download the dataset")
        with cols[0]:
            st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f'predicted_df.csv',
            mime='text/csv'
            )    
        with cols[4]:
            if st.button('Go Back'):
                st.switch_page("app.py")
    
        #data['PREDICTION'] = data['PREDICTION'].replace({1: 'DEFAULT', 0: 'NON-DEFAULT'})
        prediction_counts = data['PREDICTION'].value_counts()
        #df = prediction_counts.reset_index()

        # Rename the columns for clarity
        #df.columns = ['PREDICTION', 'Count']
        customer_types_df = pd.DataFrame({
        'Customer Type': ['Default', 'Non-default'],
        'Count of Customers': [prediction_counts.get(1, 0), prediction_counts.get(0, 0)]  # Get count of 1 and 0, defaulting to 0 if not found
        })
        
        bar_chart = alt.Chart(customer_types_df).mark_bar().encode(
            x = 'Customer Type',
            y = 'Count of Customers'
        )

        text = bar_chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-5,
            color='white'
        ).encode(text='Count of Customers:Q')
        # Display the DataFrame
        final_chart = bar_chart + text
        st.altair_chart(final_chart, use_container_width=True)

        cols2=st.columns(5)
        with cols2[4]:
            if st.button('Explainability'):
                st.switch_page("pages/2_XAI.py")
        
    else:
        st.write('Invalid Schema. Please try again.')
                    
if __name__ == "__main__":
    main()