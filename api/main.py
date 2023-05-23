from fastapi import FastAPI, HTTPException
import openai
from pydantic import BaseModel

app = FastAPI()

openai.api_key ='' # APIキーを設定する

class User(BaseModel):
    id: str
    name: str
    messages: list = []

class Message(BaseModel):
    user_id: str
    content: str

# Store for users
users = {}

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
    user.messages.append(message.content)
    chat_model = "gpt-3.5-turbo"

    if openai.api_key == '':
        response_content = "OpenAI API key is not set."
    else:
        response = openai.ChatCompletion.create(
            model=chat_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.content},
            ]
        )
        response_content = response['choices'][0]['message']['content']

    user.messages.append(response_content)
    return response_content

@app.get("/messages/{user_id}")
def read_messages(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user = users[user_id]
    return user.messages
