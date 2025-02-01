# Solana Exchange Telegram Bot 🚀

A Telegram bot that provides Solana exchange functionalities, including fetching token prices, checking wallet balances, and simulating notifications.

## Features

- **/start**: Displays a welcome message and available commands.
- **/price**: Fetches the current SOL/USDC price.
- **/wallet**: Checks the balance of a provided Solana wallet address.
- **/trade**: Placeholder for trading functionality (under development).
- **Notifications**: Simulates price change alerts.

## Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file and add your Telegram bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```
4. Run the bot:
   ```bash
   npm start
   ```

## Usage

- Start the bot by sending `/start` in Telegram.
- Use `/price` to fetch the SOL/USDC price.
- Use `/wallet <address>` to check the balance of a Solana wallet.
- Use `/trade` to see the placeholder for trading functionality.

## Notes

- Replace the placeholder chat ID in the notification example with your actual chat ID.
- Ensure the `.env` file is not publicly shared for security reasons.