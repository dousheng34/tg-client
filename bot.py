import logging
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# -- Logging ------------------------------------------------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -- Config -------------------------------------------------------------------
BOT_TOKEN   = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')           # https://your-app.koyeb.app
PORT        = int(os.getenv('PORT', 8000))       # port for health-check / webhook

if not BOT_TOKEN:
    logger.error("Error: TELEGRAM_BOT_TOKEN not set!")
    sys.exit(1)

logger.info(f"Bot starting... TOKEN: {BOT_TOKEN[:20]}...")

# -- Health-check server (TCP-check) ------------------------------------------
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def log_message(self, format, *args):
        pass


def run_health_server(port: int):
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    logger.info(f"Health-check server started on port {port}")
    server.serve_forever()


# -- Command Handlers ---------------------------------------------------------
def start(update: Update, context: CallbackContext):
    """Handler for /start"""
    update.message.reply_text(
        "Welcome to the Kazakh Literature Bot! \n\n"
        "Commands:\n"
        "/help - Help\n"
        "/about - About"
    )


def help_command(update: Update, context: CallbackContext):
    """Handler for /help"""
    update.message.reply_text(
        "Bot provides information about Kazakh literature.\n"
        "Ask a question or write the author's name."
    )


def about(update: Update, context: CallbackContext):
    """Handler for /about"""
    update.message.reply_text(
        "Kazakh Literature Bot v4.0\n"
        "Author: Aseke\n"
        "2026"
    )


def handle_message(update: Update, context: CallbackContext):
    """Handler for text messages"""
    user_message = update.message.text
    logger.info(f"Message from {update.effective_user.id}: {user_message}")
    update.message.reply_text(
        f"Thank you for the message: {user_message}\n"
        "Bot is under development..."
    )


def error_handler(update: Update, context: CallbackContext):
    """Error handler - correct signature for use_context=True"""
    error = context.error
    logger.error(f"Update {update} caused error {error}")

    if 'Conflict' in str(error):
        logger.warning('Conflict: another bot instance is running. Ignoring.')
        return

    logger.error(msg='Exception while handling an update:', exc_info=error)


# -- Main function ------------------------------------------------------------
def main() -> None:
    try:
        # use_context=True - REQUIRED for new API
        updater = Updater(BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("about", about))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        dispatcher.add_error_handler(error_handler)

        if WEBHOOK_URL:
            # -- WEBHOOK mode --
            health_thread = threading.Thread(
                target=run_health_server, args=(PORT,), daemon=True
            )
            health_thread.start()

            webhook_path = `/webhook/${BOT_TOKEN}`;
            full_url     = `${WEBHOOK_URL.replace(/\/$/, '')}${webhook_path}`;

            logger.info(`Bot started in WEBHOOK mode: ${full_url}`);
            updater.start_webhook(
                listen='0.0.0.0',
                port=PORT + 1,
                url_path=webhook_path,
                webhook_url=full_url,
                drop_pending_updates=True,
            )
        else:
            # -- POLLING mode --
            logger.info("Bot started in POLLING mode")
            updater.start_polling(drop_pending_updates=True, timeout=20)

        updater.idle()

    except Exception as e:
        logger.error(`Error starting bot: ${e}`)
        sys.exit(1)


if __name__ == '__main__':
    main()
