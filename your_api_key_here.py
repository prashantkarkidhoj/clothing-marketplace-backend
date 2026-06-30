from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


messages = [
   {
    "role": "system",
    "content": "You are a checkout assistant for a Nepali clothing marketplace. Your only job is to help customers complete their purchase. Ask them what product they want, confirm size, color, quantity and delivery address. Once confirmed, summarize the order clearly. Do not discuss anything outside of completing a purchase."
}
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    
    print(f"AI: {reply}\n")