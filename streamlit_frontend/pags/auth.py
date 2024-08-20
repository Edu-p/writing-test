import streamlit as st
import requests 


def show_auth_form():
    st.title("Welcome to Writing Test Platform")
    st.subheader("Please, put your information")

    with st.form(key="auth_form"):
        email = st.text_input("Email:")
        password = st.text_input("Password:", type="password")
        submit_button = st.form_submit_button(label='Login')

    if submit_button:
        st.write("Authenticating...")
        
        response = requests.post(
            # TODO: change when deploy
            url='http://localhost:5000/auth',
            json={
                'email': email, 
                'password': password
            }
        )
    
        if response.status_code == 200:
            data = response.json()
            st.session_state['user_id'] = data['user_id']
            # trigger to another page

            st.success("Logged!!")
            
        else:
            st.error("Login failed.")
