import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from get_attachment import get_attachment

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

def get_photos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Extract the ID from the command
    email_id = context.args[0] if context.args else None

    if email_id:
        # TODO: Implement logic to fetch photos from email using the provided ID
        # You can use the 'imaplib' library to connect to the email server and fetch emails.

        # Replace the following print statement with your email fetching logic
        print(f"Fetching photos for email ID: {email_id}")

        # TODO: Implement the logic to send photos back to the user

        update.message.reply_photo(get_attachment(), caption=f"Photos found for email ID: {email_id}")
    else:
        update.message.reply_text("Please provide an email ID. Usage: /getphotos <email_id>")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    tmp = get_attachment()
    await update.message.reply_photo(tmp)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6701709951:AAEeBV3X2lWEiQtnKR3rBaruJOJ12Uty0yw").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("getphotos", get_photos))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()