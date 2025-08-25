import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token (using environment variable for security)
BOT_TOKEN = os.getenv('BOT_TOKEN', '8419687494:AAGtcx-pnjgkqVbRQ4lny4kqXHFWqnuGj0U')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"👋 Hello {user.mention_html()}!\n"
        "I'm your Telegram bot! 🚀\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show help message\n"
        "/info - Get bot information\n"
        "/echo [text] - Echo your text\n\n"
        "Try sending me a message! 💬"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message when command /help is issued."""
    help_text = """
🤖 **Bot Help Guide**

**Commands:**
/start - Start conversation with bot
/help - Show this help message
/info - Get bot information
/echo [text] - Repeat your text

**Features:**
- Responds to messages
- Simple echo functionality
- User-friendly interface

Just send me a message and I'll respond! ✅
"""
    await update.message.reply_markdown(help_text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send bot info when command /info is issued."""
    bot_info = """
📊 **Bot Information**

**Status:** ✅ Online and working
**Token:** 🔒 Secured
**Version:** Python Telegram Bot v20.0+
**Functionality:** Basic echo bot

This bot is running successfully in VS Code! 🎉
"""
    await update.message.reply_markdown(bot_info)

async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user's text when command /echo is issued."""
    if context.args:
        text = ' '.join(context.args)
        await update.message.reply_text(f"🔊 Echo: {text}")
    else:
        await update.message.reply_text("Please provide text after /echo command. Example: /echo Hello World!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages."""
    user_text = update.message.text
    user = update.effective_user
    
    logger.info(f"User {user.first_name} said: {user_text}")
    
    response = f"📩 You said: '{user_text}'\n\nNice to chat with you! 😊"
    await update.message.reply_text(response)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors and send user-friendly message."""
    logger.error(f"Update {update} caused error: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Sorry, something went wrong. Please try again later."
        )

def main():
    """Start the bot."""
    print("🤖 Initializing Telegram Bot...")
    print(f"🔑 Token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-5:]}")
    
    try:
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("info", info_command))
        application.add_handler(CommandHandler("echo", echo_command))
        
        # Add message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Add error handler
        application.add_error_handler(error_handler)

        print("✅ Bot initialized successfully!")
        print("🔄 Starting polling for updates...")
        print("💡 Go to Telegram and send /start to your bot")
        print("⏹️  Press Ctrl+C to stop the bot")
        
        # Start polling
        application.run_polling(
            poll_interval=1.0,
            timeout=10,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Error: {e}")
        print("💡 Check your internet connection and bot token")

if __name__ == '__main__':
    main()