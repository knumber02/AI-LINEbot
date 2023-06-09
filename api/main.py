from fastapi import FastAPI, HTTPException
import openai
from pydantic import BaseModel
from .line_routes import line_router
import json
from .state import User, users



app = FastAPI()

app.include_router(line_router)
# JSONファイルを開き、値を読み込む
with open('/src/config.json') as f:
    data = json.load(f)

# JSONからAPIキーを取得
openai.api_key = data['OPENAI_API_KEY']


class User(BaseModel):
    id: str
    name: str
    personality: str = "You are an assistant that speaks like a cute girlfriend."
    messages: list = []

class Message(BaseModel):
    user_id: str
    content: str

# Store for users
# users = {'default': User(id='default', name='Default User', messages=[])}

@app.post("/users/")
def create_user(user: User):
    if user.id not in users:
        users[user.id] = user
    return user

@app.get("/users/{user_id}")
def read_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.post("/messages/")
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

            # Filter out inappropriate content (This is a simplistic approach.
            # More sophisticated content moderation may be needed depending on your use case.)
            inappropriate_words = ['inappropriate', 'offensive']
            if any(word in response_content for word in inappropriate_words):
                response_content = "I'm sorry, but I can't assist with that."

        except Exception as e:
            response_content = f"Error: {str(e)}"

    user.messages.append({"role": "assistant", "content": response_content})
    return response_content

@app.get("/messages/{user_id}")
def read_messages(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user = users[user_id]
    return user.messages

@app.put("/users/{user_id}/personality")
def set_personality(user_id: str, personality: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id].personality = personality
    return {"message": "Personality set successfully."}
