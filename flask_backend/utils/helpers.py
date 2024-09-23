from app import client_openai

def get_completion_from_messages(messages, model='gpt-4o-mini'):
    completion = client_openai.chat.completions.create(
        model=model,
        messages=messages
    )
    return completion.choices[0].message.content