import os
import requests
from requests.auth import HTTPBasicAuth
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
WC_KEY = os.environ.get('WC_KEY')
WC_SECRET = os.environ.get('WC_SECRET')

def get_products():
    url = "https://partox.ir/wp-json/wc/v3/products?per_page=5&orderby=date&order=desc"
    auth = HTTPBasicAuth(WC_KEY, WC_SECRET)
    res = requests.get(url, auth=auth)
    return res.json()

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! برای دیدن جدیدترین محصولات بنویس /new")

def new(update: Update, context: CallbackContext):
    products = get_products()
    for p in products:
        name = p["name"]
        price = p["price"]
        link = p["permalink"]
        update.message.reply_text(f"🛒 {name}\n💰 {price} تومان\n🔗 {link}")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("new", new))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
