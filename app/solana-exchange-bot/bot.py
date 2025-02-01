import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.rpc.types import TokenAccountOpts

# Environment Variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL")

# Validate Environment Variables
if not TELEGRAM_BOT_TOKEN or not SOLANA_RPC_URL:
    raise ValueError("TELEGRAM_BOT_TOKEN and SOLANA_RPC_URL environment variables must be set.")

# Initialize Solana Client
solana_client = Client(SOLANA_RPC_URL)

# Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Helper Functions
def is_valid_solana_address(address: str) -> bool:
    """Validate a Solana wallet address."""
    try:
        PublicKey(address)
        return True
    except ValueError:
        return False


# Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the /start command is issued."""
    welcome_message = """
    Welcome to the Solana Exchange Bot! 🚀
    Use the following commands to get started:
    /balance <wallet_address> - Check your Solana wallet balance
    /help - Get help and instructions
    """
    await update.message.reply_text(welcome_message)


async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check the Solana wallet balance."""
    wallet_address = context.args[0] if context.args else None

    if not wallet_address or not is_valid_solana_address(wallet_address):
        await update.message.reply_text(
            "Please provide a valid Solana wallet address. Usage: /balance <wallet_address>"
        )
        return

    try:
        balance = solana_client.get_balance(PublicKey(wallet_address))
        if 'result' in balance and 'value' in balance['result']:
            await update.message.reply_text(f"Wallet Balance: {balance['result']['value']} SOL")
        else:
            await update.message.reply_text("Failed to fetch balance. Invalid response from Solana RPC.")
    except Exception as e:
        logger.error(f"Error fetching balance: {e}")
        await update.message.reply_text("Failed to fetch balance. Please try again later.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message with instructions."""
    help_message = """
    Solana Exchange Bot Commands:
    /start - Start the bot
    /balance <wallet_address> - Check Solana wallet balance
    /help - Get help and instructions
    """
    await update.message.reply_text(help_message)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text("Sorry, I don't understand that command. Use /help for instructions.")


# Main Function
def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", check_balance))
    application.add_handler(CommandHandler("help", help_command))

    # Handle Unknown Commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()