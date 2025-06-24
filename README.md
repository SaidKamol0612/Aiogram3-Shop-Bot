# 🛒 Aiogram Shop Bot

A **Aiogram shop bot** that fetches product and category data from an external API and provides users with a clean and interactive shopping experience within Telegram.

## 📌 Features

* Fetches categories and products from an external JSON API
* User-friendly Telegram interface with inline buttons
* Browse products by category
* Shopping cart
* Multi-language support (Uz, RU)
* Easily extendable architecture (e.g., cart, checkout, admin panel)

## 🚀 Technologies Used

* Python
* `aiogram` 3
* `requests` (or `httpx`) for API calls
* External REST API for product data

## ⚙️ Setup and Run

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/shop-bot.git
cd Aiogram-Shop-Bot
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**

Create a `.env` file or update `config.py`:

```env
APP__BOT__TOKEN=your_tg_bot_token
APP__API__BASE_URL=external_api_url
APP__API__LOGIN=login_for_external_api
APP__API__PASSWORD=password_for_external_api
APP__API__PRODUCTS_ENDPOINT=external_api_products_url
APP__API__LOGIN_ENDPOINT=external_api_login_url
APP__GROUP__CHAT_ID=group_chat_id_for_orders
APP__GROUP__LINKS=[group_link_for_info,]
APP__DB__URL=database_url
APP__DB__ECHO=0
```

4. **Run the bot:**

```bash
cd src
python run.py
```

## ✅ Commands and Flow

* `/start` — Welcome message
* Inline buttons for categories
* On category selection — list of products
* On product selection — show details and action buttons (e.g., "Add to cart")

## 📄 License

This project is licensed under the MIT License.
