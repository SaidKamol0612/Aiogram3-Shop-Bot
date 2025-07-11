# Aiogram3 Shop Bot

This is a simple and efficient Telegram shop bot built with Aiogram. It fetches product data from an external API and presents it in a user-friendly format. Users can search for products using a unique product code, add items to favorites, or manage their shopping cart directly in chat. The bot is designed to be fast, lightweight, and easy to use. Ideal for small online stores or as a base for a larger e-commerce integration.

---

## 🔧 Features & Stack

**Tech Stack:**

- Python 3.11+
- [Aiogram 3](https://github.com/aiogram/aiogram)
- Async API requests (via `httpx` or `aiohttp`)
- PostgreSQL / SQLite (depending on environment)
- Docker-ready (optional)

**Core Features:**

- Product listing from external API
- Search by product sku code
- Add to favorites and shopping cart
- Basic state management via FSM
- Admin-only or open access configuration

---

## 🚀 Quick Start

1. **Clone the repository**

```bash
    git clone https://github.com/SaidKamol1912/Aiogram3-Shop-Bot.git
    cd Aiogram3-Shop-Bot
```

2. **Create and activate virtual environment**

```bash
    python -m venv venv
    source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

3. **Install dependencies**

```bash
    pip install -r requirements.txt
```

4. **Create `.env` file**

Copy `.env.example` to `.env` and fill in the values:

```env
    # Bot configurations
    BOT_CONFIG__BOT__TOKEN="your_token"

    # Database configurations
    BOT_CONFIG__DB__URL="sqlite+aiosqlite:///./db.sqlite3"
    BOT_CONFIG__DB__ECHO=1

    # External API configuration
    BOT_CONFIG__API__BASE_URL="http://example.com/api"
    BOT_CONFIG__API__LOGIN="user"
    BOT_CONFIG__API__PASSWORD="password"
    BOT_CONFIG__API__PRODUCTS_ENDPOINT="http://example.com/api/products/"
    BOT_CONFIG__API__LOGIN_ENDPOINT="http://example.com/api/login/"

    # Admin group configurations
    BOT_CONFIG__ADMIN_GROUP__CHAT_ID="-..."
```

5. **Run the bot**

```bash
    cd src
    python run.py
```

---

## 🩪 License

This project is licensed under the MIT License.
Feel free to fork, modify, or use it in your own projects.

---

## 🤝 Contributing

Open to collaboration!
Pull requests, feature ideas, and issues are welcome.

> Created with ❤️ by \[SaidKamol1912].
