import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

def interview_test():
    st.title("Chatbot Conversation - Interview Test")

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
                'type_of_test': 'interview'
            }
        )
        data = response_to_thread_id.json()
        st.session_state['thread_id'] = data['thread_id']
        thread_id = st.session_state['thread_id'] 

    if st.session_state['step_of_conversation'] == 0:
        st.session_state.conversation.append(
            "Bot: Hi! What is the project you are most proud of, and how did you contribute to it?\n")
        conversation_display = "\n".join(st.session_state.conversation)
        st.text_area("Conversation", conversation_display,
                     height=300, disabled=True)
        st.session_state['step_of_conversation'] += 1
    else:
        conversation_display = "\n".join(st.session_state.conversation)
        st.text_area("Conversation", conversation_display,
                     height=300, disabled=True)
    user_input = st.text_input(
        "Your message:", value=st.session_state['user_input'])

    if st.session_state['step_of_conversation'] < 9:
        if st.button("Send", disabled=st.session_state['send_button_clicked']):
            if user_input:
                st.session_state['send_button_clicked'] = True
                st.session_state['step_of_conversation'] += 1
                st.session_state.conversation.append(f"You: {user_input}")
                response_to_input = requests.post(
                    # TODO: change when deploy
                    url=f'{BASE_URL}/interview_chat',
                    json={
                        'user_id': user_id,
                        'thread_id': thread_id,
                        'content': user_input
                    }
                )

                data = response_to_input.json()
                llm_response = data['response']

                response = (f"Bot: {llm_response}\n")
                print(f"Bot: {llm_response}', thread_id -> {thread_id}")

                st.session_state['user_input'] = ""

                st.session_state.conversation.append(response)

                st.session_state['send_button_clicked'] = False

                st.rerun()
    else:
        time.sleep(2)

        st.session_state['page'] = 'interview_3'

        st.rerun()


