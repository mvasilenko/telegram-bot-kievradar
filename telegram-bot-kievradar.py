#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages, and sends weather map with radar meteo data in Kiev, Ukraine
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import syslog
import requests
import shutil


from PIL import Image
import numpy as np

import urllib

tmp_imagename='/tmp/RADAR_KIEV.png'
TOKEN_BOT=''

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

syslog.syslog(syslog.LOG_INFO,'telegram bot started')

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')

def radar_kiev(bot, update):

    # send typing...
    bot.sendChatAction(action=telegram.ChatAction.TYPING,chat_id=update.message.chat_id)

    pngfile="/tmp/UKBB_latest.png"
    pngtransfile="/tmp/UKBB_transparent.png"
    output="/tmp/output.png"
    mapfile="/tmp/map.png"

    # get radar black-white png
    urllib.urlretrieve("http://meteoinfo.by/radar/UKBB/UKBB_latest.png", pngfile)

    orig_color = (204,204,204,255)
    replacement_color = (255,255,255,0)
    img = Image.open(pngfile).convert('RGBA')
    data = np.array(img)

    # replace gray colors with transparent
    colors=[204,192]

    for color in colors:
      orig_color = (color,color,color,255)
      data[(data == orig_color).all(axis = -1)] = replacement_color

    img2 = Image.fromarray(data, mode='RGBA')
    img2.save(pngtransfile)

    background = Image.open(mapfile).convert('RGBA')
    foreground = Image.open(pngtransfile)

    # merge map with radar png
    background.paste(foreground,(3,10),foreground)
    background.save(output)

    # send it as answer
    with open(output,'r') as photo_file:
          update.message.reply_photo(photo_file)

def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN_BOT)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("radar_kiev", radar_kiev))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
