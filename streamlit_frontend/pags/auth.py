import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def show_auth_form():
    st.title("Welcome to Writing Test Platform")
    st.subheader("Please, put your information")

    with st.form(key="auth_form"):
        email = st.text_input("Email:")
        password = st.text_input("Password:", type="password")
        submit_button = st.form_submit_button(label='Login')

    if submit_button:
        st.write("Authenticating...")
        print(f"{BASE_URL}/auth")
        response = requests.post(
            # TODO: change when deploy
            url=f"{BASE_URL}/auth",
            json={
                'email': email,
                'password': password
            }
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state['user_id'] = data['user_id']
            st.session_state['page'] = 'choose_wtd'

            st.success("Logged!!")

            time.sleep(2)

            st.rerun()

        else:
            st.error("Login failed.")
