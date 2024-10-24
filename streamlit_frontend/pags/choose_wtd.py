import streamlit as st


def choose_what_to_do():
    st.markdown(
        """
        <style>
        .stButton > button {
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
        .stButton > button:hover {
            background-color: #e6e6e6;
            transform: scale(1.02);
        }
        /* Center and style the title */
        .wtd-title {
            text-align: center;
            color: #333333;
            font-size: 32px;
            margin-top: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="wtd-title">What do you want to do?</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        if st.button("📝 Do a New Test", key="new_test"):
            st.session_state['page'] = 'choose_wtc'
            st.rerun()

    with col2:
        if st.button("📊 View Your Metrics", key="view_metrics"):
            st.session_state['page'] = 'view_overall'
            st.rerun()
