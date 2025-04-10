from fastapi import APIRouter, HTTPException
from api.models.message import Message
from api.state import users
import openai

router = APIRouter()

@router.post("/messages/")
def create_message(message: Message):
    if message.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    user = users[message.user_id]
    user.messages.append({"role": "user", "content": message.content})
    chat_model = "gpt-3.5-turbo"

    if openai.api_key == '':
        response_content = "OpenAI API key is not set."
    else:
        # Limit the conversation history to the latest 10 messages to avoid reaching the token limit.
        conversation_history = user.messages[-10:]

        conversation_history.insert(0, {"role": "system", "content": user.personality})

        try:
            response = openai.ChatCompletion.create(
                model=chat_model,
                messages=conversation_history
            )
            response_content = response['choices'][0]['message']['content']

            # Filter out inappropriate content
            inappropriate_words = ['inappropriate', 'offensive']
            if any(word in response_content for word in inappropriate_words):
                response_content = "I'm sorry, but I can't assist with that."

        except Exception as e:
            response_content = f"Error: {str(e)}"

    user.messages.append({"role": "assistant", "content": response_content})
    return response_content

@router.get("/messages/{user_id}")
def read_messages(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user = users[user_id]
    return user.messages 
