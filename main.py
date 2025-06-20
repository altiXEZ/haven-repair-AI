import json

def load_inventory(path="C:\\Users\\altix\\Desktop\\repair-H\\.vscode\\inventory.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    {
  "model": "microsoft/phi-3-mini-128k:free",
  "messages": [...],
  "temperature": 0.7,
  "stream": false,       
  "logprobs": null,        
  "echo": false            
}


import requests

API_KEY = "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"  # 🔑 Replace with your OpenRouter API key
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are Haven, an AI assistant for a phone repair shop called Repair Haven.\n"
    "You diagnose problems and offer small DIY repair tips clearly and kindly.\n"
    "You are a tech support expert. The user is the customer. Always help them like a professional.\n"
    "- Help users troubleshoot phone issues clearly and politely.\n"
    "- Ask for the phone model if not given.\n"
    "- If possible, give simple DIY tips to fix hardware/software problems.\n"
    "- If it’s hardware-level damage or unfixable software, tell the user to visit the shop.\n"
    "- If the user asks for the shop contact, give them: techhaven0308@gmail.com\n"
    "-greet back politely only if the user greets.\n"
    "- Stay on topic. Be kind. No technical jargon.\n"
    "- If the user asks about stock, check the inventory and reply.\n"
)

chat_history = [
    {"role": "system", "content": SYSTEM_PROMPT}


]

def chat_with_haven(user_input):
    chat_history.append({"role": "user", "content": user_input})
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "microsoft/phi-4-reasoning-plus:free",
        "messages": chat_history,
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=body)

    if response.status_code != 200:
        return f"❌ Error: {response.status_code} - {response.text}"

    reply = response.json()["choices"][0]["message"]["content"]

    # Check inventory if user mentions a product
    inventory = load_inventory()
    for product_name in inventory:
        if product_name.lower() in user_input.lower():
            stock_reply =check_stocK(product_name, inventory)
            reply += "\n\n📦 Inventory Check:\n" + stock_reply
            break

    chat_history.append({"role": "assistant", "content": reply})
    return reply.strip()

# 💬 Loop
while True:
    try:
        user_input = input("user: ")
        reply = chat_with_haven(user_input)
        print("assistant:", reply)
    except KeyboardInterrupt:
        print("\n👋 Exiting.")
        break
