import json

def load_inventory(path="C:\\Users\\altix\\Desktop\\repair-H\\.vscode\\inventory.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    

from llama_cpp import Llama

# 📍 Path to your quantized model file
LLM_PATH = "C:\\Users\\altix\\Desktop\\Models\\mistral-7b-instruct-v0.1.Q4_K_M.gguf"

# ⚙️ Load model with GPU acceleration
llm = Llama(
    model_path=LLM_PATH,
    n_ctx=2048,           # Context window (2048 is standard, Mistral supports more)
    n_batch=512,          # Controls batch size for generation (safe default)
    n_threads=12,         # Adjust to your CPU core count
    n_gpu_layers=30,      # Use ~30 layers on GPU (fits in 4–5GB VRAM)
    verbose=True          # Print detailed logs (can turn off later)
)
    

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

    # 🔁 Build the full prompt including system and previous messages
    prompt = SYSTEM_PROMPT + "\n\n"
    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "Haven"
        prompt += f"{role}: {msg['content']}\n"
    prompt += "Haven:"

    # 🔍 Generate response from local LLM
    output = llm(prompt, max_tokens=512, stop=["User:", "Haven:"], temperature=0.7)
    reply = output["choices"][0]["text"].strip()

    # 📦 Inventory check
    inventory = load_inventory()
    for product_name in inventory:
        if product_name.lower() in user_input.lower():
            stock_reply = check_stock(product_name, inventory)
            reply += "\n\n📦 Inventory Check:\n" + stock_reply
            break

    chat_history.append({"role": "assistant", "content": reply})
    return reply
    reply = response.json()["choices"][0]["message"]["content"]

    # Check inventory if user mentions a product
    inventory = load_inventory()
    for product_name in inventory:
        if product_name.lower() in user_input.lower():
            stock_reply =check_stock(product_name, inventory)
            reply += "\n\n📦 Inventory Check:\n" + stock_reply
            break

    chat_history.append({"role": "assistant", "content": reply})
    return reply.strip()

def check_stock(product_name, inventory):
    stock = inventory.get(product_name, None)
    if stock is None:
        return f"Sorry, we do not have information about '{product_name}' in our inventory."
    elif stock > 0:
        return f"Yes, '{product_name}' is in stock ({stock} available)."
    else:
        return f"Sorry, '{product_name}' is currently out of stock."

# 💬 Loop
while True:
    try:
        user_input = input("user: ")
        reply = chat_with_haven(user_input)
        print("assistant:", reply)
    except KeyboardInterrupt:
        print("\n👋 Exiting.")
        break
