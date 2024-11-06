import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

BASE_URL = os.getenv('BASE_URL')


def show_auth_form():
    st.markdown(
        """
        <style>

        /* Center the content */
        .auth-container {
            max-width: 400px;
            margin: auto;
            padding-top: 50px;
        }

        /* Style the input fields */
        input {
            padding: 10px !important;
            font-size: 16px !important;
        }

        /* Style the login button */
        .login-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            width: 100%;
            cursor: pointer;
            margin-top: 20px;
        }

        .login-button:hover {
            background-color: #808080; !important /* Gray color */
        }

        /* Center and style the title */
        .auth-title {
            text-align: center;
            color: #333333;
            font-size: 32px;
            margin-bottom: 10px;
        }

        /* Center and style the subheader */
        .auth-subheader {
            text-align: center;
            color: #666666;
            font-size: 18px;
            margin-bottom: 30px;
        }

        /* Style the error message */
        .error-message {
            color: red;
            text-align: center;
            margin-top: 20px;
        }

        /* Style the success message */
        .success-message {
            color: green;
            text-align: center;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown(
            '<div class="auth-title">Welcome to the Writing Test Platform</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="auth-subheader">Please enter your login details</div>', unsafe_allow_html=True)

        with st.form(key="auth_form"):
            email = st.text_input("Email:")
            password = st.text_input("Password:", type="password")
            submit_button = st.form_submit_button(label='Login')

        if submit_button:
            with st.spinner('Authenticating...'):
                response = requests.post(
                    url=f"{BASE_URL}/auth",
                    json={
                        'email': email,
                        'password': password
                    }
                )
                time.sleep(1)

            if response.status_code == 200:
                data = response.json()
                st.session_state['user_id'] = data['user_id']
                st.session_state['page'] = 'choose_wtd'

                st.markdown(
                    '<div class="success-message">Logged in successfully!</div>', unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
            else:
                st.markdown(
                    '<div class="error-message">Login failed. Please check your credentials.</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
