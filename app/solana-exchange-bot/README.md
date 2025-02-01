# Solana Exchange Bot

A Telegram bot that allows users to check their Solana wallet balance.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/solana-exchange-bot.git
   cd solana-exchange-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your environment variables:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   SOLANA_RPC_URL=your_solana_rpc_url_here
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

- `/start` - Start the bot and see available commands.
- `/balance <wallet_address>` - Check the balance of a Solana wallet.
- `/help` - Get help and instructions.