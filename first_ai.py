from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with open("system_prompt.txt", "r") as f:
    system_prompt = f.read()

messages = [
    {"role": "system", "content": system_prompt}
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
    
    if "Onboarding complete" in reply:
        extraction_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Extract the seller information from this conversation and return ONLY a JSON object with these fields: name, shop_name, delivery_areas, product_types, instagram_page. No extra text, just the JSON."
                },
                {
                    "role": "user",
                    "content": str(messages)
                }
            ]
        )
        
        seller_data = json.loads(extraction_response.choices[0].message.content)
        
        try:
            with open("sellers.json", "r") as f:
                all_sellers = json.load(f)
        except:
            all_sellers = []
        
        all_sellers.append(seller_data)
        
        with open("sellers.json", "w") as f:
            json.dump(all_sellers, f, indent=4)
        
        print("\nSeller data saved successfully.")
        break