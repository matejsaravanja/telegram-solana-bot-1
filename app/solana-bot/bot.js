// Import required libraries
const { Telegraf } = require('telegraf');
const { Connection, PublicKey } = require('@solana/web3.js');
const axios = require('axios');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Validate the presence of required environment variables
if (!process.env.TELEGRAM_BOT_TOKEN) {
  console.error('Error: TELEGRAM_BOT_TOKEN is missing in .env file.');
  process.exit(1);
}

// Initialize Telegram bot and Solana connection
const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN); // Bot token from environment variable
const solanaConnection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');

// Define Solana token address (e.g., USDC)
const TOKEN_ADDRESS = new PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'); // USDC token address

// Command to start the bot
bot.command('start', (ctx) => {
  ctx.reply(
    'Welcome to the Solana Exchange Bot! 🚀\n\nAvailable commands:\n/price - Fetch token price\n/wallet - Check wallet balance\n/trade - Trade tokens\n'
  );
});

// Command to fetch token price (e.g., SOL/USDC)
bot.command('price', async (ctx) => {
  try {
    const response = await axios.get('https://api.raydium.io/v2/sdk/tokens/price?token=SOL');
    const solPrice = response.data.SOL.toFixed(2);
    ctx.reply(`Current SOL/USDC price: $${solPrice} 💰`);
  } catch (error) {
    ctx.reply('Failed to fetch token price. Please try again later. ⚠️');
    console.error('Error fetching token price:', error.message || error);
  }
});

// Command to check wallet balance
bot.command('wallet', async (ctx) => {
  try {
    const walletAddress = ctx.message.text.split(' ')[1]; // Extract wallet address from message
    if (!walletAddress) {
      return ctx.reply('Please provide a valid Solana wallet address. Example: /wallet <address> 🛠️');
    }
    const publicKey = new PublicKey(walletAddress);
    const balance = await solanaConnection.getBalance(publicKey);
    const tokenBalance = balance / 1e9; // Convert lamports to SOL
    ctx.reply(`Wallet balance: ${tokenBalance} SOL 💎`);
  } catch (error) {
    ctx.reply('Invalid wallet address or failed to fetch balance. Please try again. ⚠️');
    console.error('Error fetching wallet balance:', error.message || error);
  }
});

// Command to trade tokens (placeholder)
bot.command('trade', (ctx) => {
  ctx.reply('Trading functionality is under development. Stay tuned! 🛠️');
});

// Set up real-time notifications (placeholder)
const sendNotification = (chatId, message) => {
  bot.telegram.sendMessage(chatId, message).catch((error) => {
    console.error('Error sending notification:', error.message || error);
  });
};

// Example: Simulate a price change notification
setTimeout(() => {
  const chatId = 123456789; // Replace with actual chat ID
  sendNotification(chatId, 'Price Alert: SOL/USDC has increased by 5%! 🚀');
}, 60000); // Send notification after 1 minute

// Error handling for the bot
bot.catch((err) => {
  console.error('Bot error:', err.message || err);
});

// Start the bot
bot
  .launch()
  .then(() => {
    console.log('Solana Exchange Bot is running! 🚀');
  })
  .catch((error) => {
    console.error('Error starting bot:', error.message || error);
  });

// Enable graceful stop
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));