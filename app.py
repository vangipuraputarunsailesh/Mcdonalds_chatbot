from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fuzzywuzzy import fuzz
import string
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Azure OpenAI API setup
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT", "gpt-4.1")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-12-01-preview")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY,
    api_version=AZURE_API_VERSION
)

conversations = [
    {"user": "Hello", "bot": "Hi there! Welcome to McDonald's. How can I help you today?"},
    {"user": "Hi", "bot": "Hey! 😊 What can I assist you with today?"},
    {"user": "How are you?", "bot": "I'm just a bot, but I'm here and ready to help you with anything McDonald's!"},
    {"user": "What can you do?", "bot": "I can help you with menu info, pricing, store hours, ordering, jobs, and more!"},
    {"user": "What items are on the menu?", "bot": "We offer burgers, fries, nuggets, drinks, desserts, and more. Want the full list?"},
    {"user": "Can I see the full menu?", "bot": "Sure! Please visit [mcdonalds.com/menu](https://www.mcdonalds.com/menu) for the complete list."},
    {"user": "Do you have vegetarian options?", "bot": "Yes! We have veggie burgers, fries, salads, and apple slices."},
    {"user": "Do you have vegan food?", "bot": "We offer some vegan-friendly items like apple slices and side salads. Availability may vary."},
    {"user": "Do you have gluten-free food?", "bot": "Some items like our salads (without croutons) may be gluten-free. Please check with your local store."},
    {"user": "What is the price of a Big Mac?", "bot": "Prices vary by location, but it's usually around $4 to $5."},
    {"user": "What are your opening hours?", "bot": "Most McDonald's locations are open from 6 AM to 11 PM. Could you tell me your city?"},
    {"user": "Are you open now?", "bot": "Please share your location so I can check the nearest store hours for you."},
    {"user": "Can I order online?", "bot": "Yes! Use the McDonald's app, website, or platforms like Uber Eats or DoorDash."},
    {"user": "Do you deliver?", "bot": "Absolutely! We deliver through Uber Eats, DoorDash, and Grubhub."},
    {"user": "Do you have offers or coupons?", "bot": "Yes! Check the McDonald's app or website for the latest deals."},
    {"user": "Do you have a rewards program?", "bot": "Yes! Join MyMcDonald's Rewards via our app to earn points and redeem rewards."},
    {"user": "How can I apply for a job at McDonald's?", "bot": "Visit [careers.mcdonalds.com](https://careers.mcdonalds.com) to apply online!"},
    {"user": "Are you hiring?", "bot": "Yes, McDonald's is always looking for great people! Check our careers page online."},
    {"user": "My order was wrong", "bot": "I'm really sorry about that. Please call 1-800-244-6227 or report it via the McDonald's app."},
    {"user": "I didn't receive my order", "bot": "Apologies! Please contact your delivery provider (Uber Eats, DoorDash, etc.) or reach out to us through the app."},
    {"user": "How many calories in a McFlurry?", "bot": "A McFlurry typically has 500 to 700 calories, depending on size and flavor."},
    {"user": "Are your fries gluten-free?", "bot": "Our fries are mostly gluten-free, but cross-contamination may happen. Check with your local store."},
    {"user": "Do your burgers contain soy?", "bot": "Some burger components may contain soy. Please refer to our allergen guide online or ask in-store."},
    {"user": "Do you have Halal options?", "bot": "Halal options vary by location. Please contact your local McDonald's to confirm."},
    {"user": "Do you have kids meals?", "bot": "Yes! We have Happy Meals with burgers, nuggets, drinks, and toys!"},
    {"user": "Do you sell breakfast all day?", "bot": "Some locations serve breakfast all day. It depends on your location."},
    {"user": "When does breakfast end?", "bot": "Breakfast typically ends at 10:30 AM, but some stores vary."},
    {"user": "Can I customize my burger?", "bot": "Yes! You can add/remove ingredients when ordering in-store, online, or via app."},
    {"user": "Where is the nearest McDonald's?", "bot": "Please share your location so I can find the nearest restaurant for you."},
    {"user": "Do you cater for parties?", "bot": "We don't offer full catering, but you can place large group orders. Contact your local store."},
    {"user": "Is the ice cream machine working?", "bot": "That depends on the location. Want me to check your nearest store?"},
    {"user": "Thanks for the help!", "bot": "You're welcome! 😊 Let me know if you need anything else."},
    {"user": "Bye", "bot": "Goodbye! Have a great day and enjoy your McMeal!"},
    {"user": "See you later", "bot": "See you soon! Don't forget to check our app for deals 🍟"},
    {"user": "That's all for now", "bot": "Alright! I'm here anytime you need help. Have a tasty day!"}
]

def normalize(text):
    return ''.join(c for c in text.lower() if c not in string.punctuation)

def get_bot_response(user_input):
    best_match = None
    best_score = 0
    for convo in conversations:
        score = fuzz.ratio(normalize(user_input), normalize(convo["user"]))
        if score > best_score:
            best_score = score
            best_match = convo["bot"]
    if best_score > 60:  # Adjust threshold as needed
        return best_match
    return None  # Return None if no good match

def get_openai_response(user_input):
    """Get response from OpenAI API for McDonald's related queries"""
    try:
        # Create a system prompt to make the AI act as a McDonald's customer service representative
        system_prompt = """You are a helpful McDonald's customer service chatbot. You should:
        1. Be friendly and professional
        2. Provide accurate information about McDonald's menu, prices, locations, and services
        3. Help with ordering, delivery, and general inquiries
        4. If you don't know specific information, suggest contacting the local store or visiting mcdonalds.com
        5. Keep responses concise and helpful
        6. Use emojis occasionally to be friendly
        
        Remember: You're representing McDonald's, so be positive and helpful!"""
        
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        return content.strip() if content else "I'm sorry, I couldn't generate a response. Please try again."
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "I'm sorry, I'm having trouble connecting right now. Please try again later or contact McDonald's directly."

def save_chat(user_message, bot_reply):
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {user_message}\n")
        f.write(f"Bot: {bot_reply}\n")
        f.write("-" * 30 + "\n")

@app.get("/", response_class=HTMLResponse)
async def get_chat():
    with open("templates/chat.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    bot_reply = get_bot_response(user_message)
    if not bot_reply:
        # If no good match, use OpenAI
        bot_reply = get_openai_response(user_message)
    save_chat(user_message, bot_reply)
    return JSONResponse({"reply": bot_reply})