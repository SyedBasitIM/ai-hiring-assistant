import os

from mistralai import Mistral

from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    api_key = os.getenv('MISTRAL_API_KEY')
    if api_key is None:
        print('You need to set your MISTRAL_API_KEY environment variable')
        exit(1)
    else:
        # print(f'This is the key {api_key}')
        pass

    model = "mistral-large-latest"
    client = Mistral(api_key=api_key)
    # client.chat.stream()

    messages = [
        {"role": "user", "content": "Who is the best cricketer after internation debut in 2000? Just give their names"}
    ]

# Get chat completion
# chat_response = client.chat.complete(
#     model=model,
#     messages=messages
# )
# print(chat_response.choices[0].message.content)

# Get chat completion with streaming
# chat_response = client.chat.complete(
#     model=model,
#     messages=messages,
#     stream=True  # Enable streaming
# )

# Process the streaming response
# for chunk in chat_response:
#     # Print each chunk of the response as it is received
#     if chunk.choices:
#         print(chunk.choices[0].delta.content, end='', flush=True)
try:
    chat_response = client.chat.stream(
        model=model,
        messages=messages
    )

    # Process the streaming response
    for chunk in chat_response:
        # if chunk.choices and chunk.choices[0].delta.content is not None:
        print(chunk.data.choices[0].delta.content, end='')

except Exception as e:
    print(f"An error occurred: {e}")

# for chunk in stream_response:
# Print each piece of the response as it comes
# 'delta' contains the current partial output being generated
# 'print(..., end="", flush=True)' makes it appear like live typing
# print(chunk.data.choices[0].delta.content)