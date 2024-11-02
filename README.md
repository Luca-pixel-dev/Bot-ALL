# @all Mention Bot for Active Chat Members

This Telegram bot allows users to mention all active chat members who have recently sent messages using the `@all` command. The bot tracks active users and enables mentioning them with a cooldown to prevent spam.

## Features

- The `@all` command mentions all active chat members with usernames.
- Cooldown: A user can only use the `@all` command once every 5 minutes to prevent spam.

## Requirements

- Python 3.11
- `python-telegram-bot` library
- `.env` file to store the bot token

## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment** (recommended):

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
    ```

3. **Install dependencies**:

    ```bash
    pip install python-telegram-bot python-dotenv
    ```

4. **Set up the bot token**:
   - Create a `Token.env` file in the root project directory.
   - Add your bot token to `Token.env`:

    ```env
    TELEGRAM_BOT_TOKEN=your-telegram-bot-token
    ```

## Usage

1. **Start the bot**:

    ```bash
    python bot.py
    ```

2. **Commands**:

   - `@all` — The bot will respond by tagging all active chat members who have sent messages and have a username.

3. **Usage Examples**:

    - When a user sends `@all`, the bot will mention all active users in the chat.
    - If a user tries to use `@all` again within 5 minutes, the bot will notify them of the remaining cooldown time.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
