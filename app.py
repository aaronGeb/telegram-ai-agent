from fastapi import FastAPI, Request
from telegram import Bot
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Configure Gemini using the new google-genai SDK
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Configure Telegram Bot
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

# In-memory chat sessions per user (chat_id - Chat object)
# The Chat object natively tracks conversation history
chat_sessions = {}

SYSTEM_PROMPT = "You are a helpful, friendly AI assistant. Be concise and clear."


def get_or_create_chat(chat_id: int):
    """Get existing chat session or create a new one for this user."""
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=1024,
            ),
        )
    return chat_sessions[chat_id]


async def get_ai_response(chat_id: int, user_message: str) -> str:
    """Send message to Gemini via a persistent chat session and return the reply."""
    chat = get_or_create_chat(chat_id)
    response = chat.send_message(user_message)
    return response.text.strip()


@app.get("/")
async def root():
    return {"status": "Telegram AI Agent is running 🤖"}


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    # Ignore non-message updates
    if "message" not in data:
        return {"status": "ignored"}

    message = data["message"]
    chat_id = message["chat"]["id"]
    user_message = message.get("text", "")

    # Ignore empty messages or non-text (e.g. stickers)
    if not user_message:
        return {"status": "ignored"}

    # Handle /start command
    if user_message == "/start":
        welcome = (
            "👋 Hello! I'm your AI assistant powered by Gemini.\n\n"
            "Just send me any message and I'll reply!\n\n"
            "Commands:\n"
            "/start - Show this message\n"
            "/clear - Clear conversation history"
        )
        await bot.send_message(chat_id=chat_id, text=welcome)
        return {"status": "ok"}

    # Handle /clear command
    if user_message == "/clear":
        chat_sessions.pop(chat_id, None)
        await bot.send_message(
            chat_id=chat_id, text="🗑️ Conversation history cleared! Starting fresh."
        )
        return {"status": "ok"}

    # Show typing indicator
    await bot.send_chat_action(chat_id=chat_id, action="typing")

    # Get AI response
    ai_reply = await get_ai_response(chat_id, user_message)

    # Send reply back to Telegram
    await bot.send_message(chat_id=chat_id, text=ai_reply)

    return {"status": "ok"}
