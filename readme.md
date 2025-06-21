# 🤖 Telegram Bot Template

Ready-to-use Telegram bot template with FastAPI, Redis, and Docker for rapid development startup.

## ⚡ Features

- **FastAPI** - for API, miniapp, webhook
- **Redis** - state management, caching
- **Docker** - containerization of redis and bot (ngrok is used in dev profile)
- **Aiogram**

## 🏗️ Project Structure

```
bot/
├── handlers/          # Message handlers
├── keyboards/         # Keyboards (inline and default)
├── services/          # Services (Redis, HTTP client)
├── filters/           # Validation filters
├── state/             # FSM states
├── server/            # FastAPI server with webhook, miniapp, api
├── texts/             # Message texts
├── data/              # Configuration and logs
└── utils/             # Helper utilities
```

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bulb1k/tgbot-template.git
   cd telegram-bot-template
   ```

2. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit the .env file with your settings
   ```

3. **Run with Docker**
   ```bash
   docker-compose up -d
   ```
