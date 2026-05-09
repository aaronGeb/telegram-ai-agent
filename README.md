# 🤖 Telegram AI Agent

A Telegram bot powered by **Google Gemini 2.0 Flash** and **FastAPI**, exposed to the internet via **ngrok**.

Send any message to the bot and get an instant AI-generated reply with full conversation memory per user.

---

## Architecture

```
Telegram User
     ↓
Telegram Bot API
     ↓
ngrok (exposes local server)
     ↓
FastAPI Webhook (/webhook)
     ↓
Gemini 2.0 Flash API
     ↓
Telegram Response
```

---

## Tech Stack

| Tool                  | Purpose                                        |
| --------------------- | ---------------------------------------------- |
| `FastAPI`             | Webhook server that receives Telegram messages |
| `python-telegram-bot` | Send and receive Telegram messages             |
| `google-genai`        | Google Gemini 2.0 Flash AI responses           |
| `ngrok`               | Expose local server to the internet            |
| `python-dotenv`       | Load API keys from `.env` file                 |

---

## 🚀 Setup Instructions

### 1. Clone / enter the project folder

```bash
cd telegram-ai-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get your API keys

**Gemini API key:**

- Go to https://aistudio.google.com
- Create an API key

**Telegram Bot Token:**

- Open Telegram → search `@BotFather`
- Send `/newbot` and follow the steps
- Copy the token it gives you

### 5. Fill in your `.env` file

```env
GEMINI_API_KEY=your_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

### 6. Run the server

```bash
# 80 (requires sudo on Mac/Linux)
sudo uvicorn app:app --reload --port 80
```

### 7. Expose with ngrok

```bash


# running on port 80
ngrok http 80
```

Copy your HTTPS forwarding URL, e.g.:

```
https://abcd.ngrok-free.app
```

### 8. Register the webhook with Telegram

Paste this in your browser (replace the values):

```
https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://YOUR_NGROK_URL/webhook
```

You should see:

```json
{ "ok": true, "result": true }
```

### 9. Test it!

Open your bot on Telegram and send any message. Gemini will reply!

---

## 💬 Bot Commands

| Command  | Action                              |
| -------- | ----------------------------------- |
| `/start` | Show welcome message                |
| `/clear` | Clear your conversation history     |
| Any text | Get an AI-powered reply from Gemini |

---

## Common Errors

| Error                         | Fix                                                                              |
| ----------------------------- | -------------------------------------------------------------------------------- |
| `404 Not Found` on webhook    | Make sure URL starts with `bot` — `https://api.telegram.org/botTOKEN/...`        |
| `500 Internal Server Error`   | Check your `.env` keys are correct and server is running                         |
| `429 RESOURCE_EXHAUSTED`      | Gemini free tier quota hit — wait a minute or add billing at aistudio.google.com |
| ngrok tunneling to wrong port | Run `ngrok http 8000` not `ngrok http 80` unless server is on port 80            |

---

## Next Steps

- [ ] Add PostgreSQL for persistent memory across server restarts
- [ ] Add LangChain tools (web search, calculator)
- [ ] Add voice message support
- [ ] Add PDF/document uploads
- [ ] Deploy on Render or Railway (no more ngrok needed)
- [ ] Build a Job Hunting Agent on top of this
