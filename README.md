# McDonald's Chatbot with Azure OpenAI Integration

A FastAPI-based chatbot that provides McDonald's customer service using a combination of predefined responses and Azure OpenAI's GPT model for dynamic interactions.

## Features

- 🤖 Hybrid response system (predefined + AI-powered)
- 🔐 Secure API key management using environment variables
- 💬 Real-time chat interface
- 📝 Chat history logging
- 🍔 McDonald's-specific knowledge base

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI

1. Get your Azure OpenAI endpoint and API key from your Azure portal
2. Open the `.env` file in your project directory
3. Update the Azure OpenAI configuration:

```
AZURE_ENDPOINT=https://your-resource-name.region.cognitiveservices.azure.com/
AZURE_API_KEY=your-azure-api-key-here
AZURE_DEPLOYMENT=gpt-4.1
AZURE_API_VERSION=2024-12-01-preview
```

### 3. Run the Application

```bash
uvicorn app:app --reload
```

The chatbot will be available at `http://localhost:8000`

## How It Works

1. **Predefined Responses**: The chatbot first tries to match user input with predefined McDonald's-related Q&A pairs using fuzzy string matching.

2. **Azure OpenAI Fallback**: If no good match is found (similarity score < 60%), the chatbot uses Azure OpenAI's GPT model to generate a contextual response.

3. **System Prompt**: The AI is configured with a McDonald's-specific system prompt to ensure responses are relevant and professional.

## File Structure

```
Mcdonalds_chatbot/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (API keys)
├── .gitignore         # Git ignore rules
├── README.md          # This file
├── static/            # Static files (CSS, JS, images)
│   └── logo.png
├── templates/         # HTML templates
│   └── chat.html
└── chat_history.txt   # Chat logs (auto-generated)
```

## Security Notes

- ✅ Azure OpenAI credentials are stored in `.env` file (not committed to git)
- ✅ `.env` file is included in `.gitignore`
- ✅ Error handling prevents API key exposure

## Customization

You can customize the chatbot by:

1. **Adding more predefined responses** in the `conversations` list in `app.py`
2. **Modifying the system prompt** in the `get_openai_response` function
3. **Adjusting the similarity threshold** (currently 60%) in `get_bot_response`
4. **Changing the Azure OpenAI deployment** in the `.env` file

## API Endpoints

- `GET /` - Chat interface
- `POST /chat` - Chat endpoint (accepts JSON with "message" field)

## Troubleshooting

1. **API Key Issues**: Make sure your Azure OpenAI API key is valid and has sufficient credits
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Port Issues**: If port 8000 is busy, use `uvicorn app:app --reload --port 8001`

## License

This project is for educational purposes. Please ensure compliance with Azure OpenAI's terms of service and McDonald's brand guidelines. 