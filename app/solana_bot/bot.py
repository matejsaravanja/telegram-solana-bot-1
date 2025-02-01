import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.system_program import TransferParams, transfer
from solana.transaction import Transaction
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Solana RPC client
SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL', 'https://api.mainnet-beta.solana.com')
client = Client(SOLANA_RPC_URL)

# Wallets (for testing purposes, use secure storage in production)
WALLETS = {}

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the Solana Telegram Bot! Use /help to see available commands."
    )

# Help command
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Available commands:\n"
        "/balance <public_key> - Get wallet balance\n"
        "/send <to_public_key> <amount> - Send SOL tokens\n"
        "/monitor <public_key> - Monitor transactions for a wallet\n"
        "/register <public_key> - Register your wallet"
    )

# Get wallet balance
def balance(update: Update, context: CallbackContext) -> None:
    try:
        args = update.message.text.split()
        if len(args) < 2:
            update.message.reply_text("Please provide a public key.")
            return

        public_key = args[1]
        balance = client.get_balance(PublicKey(public_key)).get('result', {}).get('value', 0)
        update.message.reply_text(f"Wallet Balance: {balance / 1e9} SOL")
    except Exception as e:
        logger.error(f"Error fetching balance: {e}")
        update.message.reply_text("Error fetching balance. Please check the public key.")

# Send SOL tokens
def send(update: Update, context: CallbackContext) -> None:
    try:
        args = update.message.text.split()
        if len(args) < 3:
            update.message.reply_text("Please provide a recipient public key and amount.")
            return

        to_public_key = args[1]
        amount = float(args[2]) * 1e9  # Convert SOL to lamports

        # Fetch wallet from storage (for testing purposes)
        from_public_key = WALLETS.get(update.message.from_user.id)
        if not from_public_key:
            update.message.reply_text("No wallet associated with your account. Use /register to add one.")
            return

        # Create and send transaction
        txn = Transaction().add(transfer(TransferParams(
            from_pubkey=PublicKey(from_public_key),
            to_pubkey=PublicKey(to_public_key),
            lamports=int(amount)
        )))
        response = client.send_transaction(txn, opts=TxOpts(skip_preflight=True, commitment=Confirmed))

        if response.get('result'):
            update.message.reply_text(f"Transaction successful! TxID: {response['result']}")
        else:
            update.message.reply_text("Transaction failed. Please try again.")
    except Exception as e:
        logger.error(f"Error sending tokens: {e}")
        update.message.reply_text("Error sending tokens. Please check the inputs.")

# Register wallet (for testing purposes)
def register(update: Update, context: CallbackContext) -> None:
    try:
        args = update.message.text.split()
        if len(args) < 2:
            update.message.reply_text("Please provide a public key.")
            return

        public_key = args[1]
        WALLETS[update.message.from_user.id] = public_key
        update.message.reply_text(f"Wallet registered: {public_key}")
    except Exception as e:
        logger.error(f"Error registering wallet: {e}")
        update.message.reply_text("Error registering wallet. Please check the public key.")

# Monitor transactions
def monitor(update: Update, context: CallbackContext) -> None:
    try:
        args = update.message.text.split()
        if len(args) < 2:
            update.message.reply_text("Please provide a public key.")
            return

        public_key = args[1]
        response = client.get_confirmed_signature_for_address2(PublicKey(public_key), limit=5)
        transactions = response.get('result', [])
        if transactions:
            update.message.reply_text(f"Recent transactions for wallet {public_key}:\n" +
                                     "\n".join([f"TxID: {tx['signature']}" for tx in transactions]))
        else:
            update.message.reply_text("No recent transactions found for this wallet.")
    except Exception as e:
        logger.error(f"Error monitoring transactions: {e}")
        update.message.reply_text("Error monitoring transactions. Please check the public key.")

# Error handler
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update "{update}" caused error "{context.error}"')

# Main function
def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("balance", balance))
    dispatcher.add_handler(CommandHandler("send", send))
    dispatcher.add_handler(CommandHandler("register", register))
    dispatcher.add_handler(CommandHandler("monitor", monitor))

    # Log errors
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()