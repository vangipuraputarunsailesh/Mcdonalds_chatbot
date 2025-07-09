import string

conversations = [
    {"user": "Hello", "bot": "Hi there! Welcome to McDonald's. How can I help you today?"},
    {"user": "Hi", "bot": "Hey! 😊 What can I assist you with today?"},
    {"user": "How are you?", "bot": "I'm just a bot, but I'm here and ready to help you with anything McDonald's!"},
    {"user": "What can you do?", "bot": "I can help you with menu info, pricing, store hours, ordering, jobs, and more!"},
    {"user": "What items are on the menu?", "bot": "We offer burgers, fries, nuggets, drinks, desserts, and more. Want the full list?"},
    {"user": "Do you have vegetarian options?", "bot": "Yes! We have veggie burgers, fries, salads, and apple slices."},
    {"user": "What is the price of a Big Mac?", "bot": "Prices vary by location, but it’s usually around $4 to $5."},
    {"user": "What are your opening hours?", "bot": "Most McDonald’s locations are open from 6 AM to 11 PM. Could you tell me your city?"},
    {"user": "Is McDonald's open now?", "bot": "Please share your location so I can find the nearest store hours for you."},
    {"user": "Can I order online?", "bot": "Yes! Use the McDonald’s app, our website, or platforms like Uber Eats or DoorDash."},
    {"user": "Do you offer home delivery?", "bot": "Absolutely! We partner with delivery services like Uber Eats, DoorDash, and Grubhub."},
    {"user": "Are there any offers or coupons?", "bot": "Yes! You can find the latest deals in the McDonald’s app or on our website."},
    {"user": "How can I apply for a job at McDonald’s?", "bot": "Visit [careers.mcdonalds.com](https://careers.mcdonalds.com) to apply online!"},
    {"user": "My order was wrong.", "bot": "I’m really sorry about that. Please call 1-800-244-6227 or report it via the McDonald’s app."},
    {"user": "How many calories are in a McFlurry?", "bot": "A McFlurry typically has 500 to 700 calories, depending on the size and flavor."},
    {"user": "Do your fries contain gluten?", "bot": "Our fries are mostly gluten-free, but cross-contamination may happen. Check with your local store to be sure."},
    {"user": "Thanks for the help!", "bot": "You're welcome! 😊 Let me know if you need anything else."},
    {"user": "Bye", "bot": "Goodbye! Have a great day and enjoy your McMeal!"},
    {"user": "See you later", "bot": "See you soon! Don’t forget to check our app for deals 🍟"},
    {"user": "That’s all for now", "bot": "Alright! I'm here anytime you need help. Have a tasty day!"}
]

def normalize(text):
    # Lowercase, remove punctuation
    return ''.join(c for c in text.lower() if c not in string.punctuation)

def get_bot_response(user_input):
    norm_input_words = set(normalize(user_input).split())
    best_match = None
    best_score = 0
    for convo in conversations:
        norm_key_words = set(normalize(convo["user"]).split())
        # Count how many words overlap
        score = len(norm_input_words & norm_key_words)
        if score > best_score:
            best_score = score
            best_match = convo["bot"]
    # If at least one word matches, return the best match
    if best_score > 0:
        return best_match
    return "Welcome to McDonald's. How may I assist you?"

print("Welcome to McDonald's Chatbot! (Type 'exit' to quit)")
while True:
    user_input = input("You: ")
    if normalize(user_input) in ['exit', 'quit', 'bye']:
        print("Bot: Goodbye! Have a great day and enjoy your McMeal!")
        break
    response = get_bot_response(user_input)
    print("Bot:", response)
    
#python -m uvicorn app:app --reload
#http://127.0.0.1:8000