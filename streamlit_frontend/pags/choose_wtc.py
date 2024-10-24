import streamlit as st


def choose_what_type_of_chat():
    st.markdown(
        """
        <style>
        /* Style the back button */
        .back-button .stButton > button {
            background-color: #f0f0f0;
            color: #333333;
            border: none;
            font-size: 18px;
            cursor: pointer;
            padding: 10px 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            width: auto;
        }
        .back-button .stButton > button:hover {
            background-color: #e0e0e0;
        }

        /* Center and style the title */
        .wtc-title {
            text-align: center;
            color: #333333;
            font-size: 32px;
            margin-top: 30px;
            margin-bottom: 40px;
        }

        /* Style the option buttons */
        .option-buttons .stButton > button {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 40px;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            width: 100%;
            margin: 10px;
            font-size: 22px;
            font-weight: bold;
            color: #333333;
        }
        .option-buttons .stButton > button:hover {
            background-color: #e6e6e6;
            transform: scale(1.02);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("← Back", key="back"):
        st.session_state['page'] = 'choose_wtd'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="wtc-title">Choose the type of situation you want to be tested on</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="option-buttons">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        if st.button("📝 Report Activity Situation", key="report_activity"):
            st.session_state['page'] = 'report_activity_1'
            st.rerun()

    with col3:
        if st.button("💼 Interview Situation", key="interview"):
            st.session_state['page'] = 'interview_1'
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
