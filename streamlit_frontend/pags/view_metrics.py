import streamlit as st

def view_overall_metrics():
    st.title('')
    
    # verifications in session state 

    st.markdown(f"<h2 style='font-size:30px;'>{}</h2>", unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.markdown("""
        <style>
        div.stButton > button {
            width: 100%; 
            height: 100px; 
            font-size: 70px; 
            margin: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("button"):
        st.write("clicked")

view_overall_metrics()