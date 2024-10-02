import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

# os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def report_test():
    st.title("Chatbot Conversation - Report Test")

    # verifications in session state
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = ''
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = None
    if 'step_of_conversation' not in st.session_state:
        st.session_state['step_of_conversation'] = 0
    if 'send_button_clicked' not in st.session_state:
        st.session_state['send_button_clicked'] = False
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ""
    if "last_correction" not in st.session_state:
        st.session_state['last_correction'] = "No correction yet."

    # get thread_id to start conversation
    user_id = st.session_state['user_id']
    thread_id = st.session_state['thread_id']

    if thread_id:
        print('Thread ID exists:', thread_id)
    else:
        response_to_thread_id = requests.post(
            # TODO: change when deploy
            url=f'{BASE_URL}/get_conversation',
            json={
                'user_id': user_id,
                'type_of_test': 'report'
            }
        )
        data = response_to_thread_id.json()
        st.session_state['thread_id'] = data['thread_id']
        thread_id = st.session_state['thread_id']

    if st.session_state['step_of_conversation'] == 0:
        st.session_state.conversation.append(
            "Bot: Hi! I'm your tech lead. Can you tell me what you did?\n")
        conversation_display = "\n".join(st.session_state.conversation)
        st.text_area("Conversation", conversation_display,
                     height=300, disabled=True)
        st.session_state['step_of_conversation'] += 1

        st.text_area("Correction of last message", 'No correction received yet.', height=100, disabled=True)
    else:
        conversation_display = "\n".join(st.session_state.conversation)
        st.text_area("Conversation", conversation_display,
                     height=300, disabled=True)
        
        last_correction = st.session_state.get('last_correction', 'No correction received yet.')
        st.text_area("Correction of last message", last_correction, height=100, disabled=True)

    user_input = st.text_input(
        "Your message:", value=st.session_state['user_input'])

    if st.session_state['step_of_conversation'] < 4:
        if st.button("Send", disabled=st.session_state['send_button_clicked']):
            if user_input:
                st.session_state['send_button_clicked'] = True
                st.session_state['step_of_conversation'] += 1
                st.session_state.conversation.append(f"You: {user_input}")
                response_to_input = requests.post(
                    # TODO: change when deploy
                    url=f'{BASE_URL}/chat',
                    json={
                        'user_id': user_id,
                        'thread_id': thread_id,
                        'content': user_input
                    }
                )

                if response_to_input.status_code == 200:
                    data = response_to_input.json()
                    llm_response = data['response']
                    llm_correction = data['corr']

                    response = (f"Bot: {llm_response}\n")
                    print(f"Bot: {llm_response}', thread_id -> {thread_id}")

                    st.session_state['user_input'] = ""

                    st.session_state.conversation.append(response)

                    st.session_state['last_correction'] = llm_correction

                    st.session_state['send_button_clicked'] = False

                    st.rerun()
                else:
                    st.error('Error in response from backend')   
    else:
        time.sleep(2)

        st.session_state['page'] = 'report_activity_3'

        st.rerun()
