from openai_client import client_openai


def get_completion_from_messages(messages, model='gpt-4o'):
    completion = client_openai.chat.completions.create(
        model=model,
        messages=messages
    )
    return completion.choices[0].message.content
