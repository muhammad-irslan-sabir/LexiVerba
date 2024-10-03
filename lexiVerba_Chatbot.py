import os
import openai
from pydantic import BaseModel 
from fastapi import FastAPI
import uvicorn

import nest_asyncio
nest_asyncio.apply()

from nemoguardrails import RailsConfig, LLMRails

app = FastAPI()

os.environ["OPENAI_API_KEY"] = "sk-qfkpJj1iHvdyumLr7FfJTDH5DZXRuuRS1evn8WESuKT3BlbkFJLgCDg-PbarEP8CyxVwIhz8vRdO00GMfhclpojmMTEA"

try:
    config = RailsConfig.from_path("C:\\Python_Codes\\Python_Data\\Sending_Mail_Using_Python\\LexiVerba_rag.yaml")
    rails = LLMRails(config)
except Exception as e:
    print(f"Error loading nemoguardrails configuration: {e}")

#@app.get("/")
#async def read_root():
#    return {"message": "Welcome to the LexiVerba Chatbot API! Use the /chatbot/ endpoint to interact with the bot."}

class UserInput(BaseModel):
    message: str

@app.post("/chatbot/")
async def chatbot(user_input: UserInput):
    try:
        response = rails.generate(messages=[{
            "role": "user",
            "content": user_input.message
        }])
        return {"response": response["content"]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("lexiVerba_Chatbot:app", host="0.0.0.0", port=8001, reload=True, log_level="debug")
