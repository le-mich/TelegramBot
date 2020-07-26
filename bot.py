import logging, sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import time, datetime

# import sensitive elements from separated python document
from instanceElements import TK as TOKEN
from instanceElements import GID as GROUPID

# command use only functions
def command(update, context):
    context.bot.sendMessage(chat_id=update.effective_chat.id, text='stuff to send to the chat')

def help(update, context):
    context.bot.sendMessage(chat_id=update.effective_chat.id, text="""/time - dispays the current time
/command - calls the "command" command
/help - shows this message""")

# mixed use functions: can be called as a command from a user or automatically as a planned callback
def timeMixed(context, chat = GROUPID):
    context.bot.sendMessage(chat_id = chat, text = datetime.now().strftime("%A %d/%m/%y, %H:%M"))

# commands and callbacks: wrapping of the mixed use functions as actual commands or callbacks
def timeMixed_command(update, context):
    timeMixed(context, chat = update.effective_chat.id)

def timeMixed_callback(context: CallbackContext):
    timeMixed(context)

# fallback function: called when passed an unknown command
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Wut?')


def main():
    global updater

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # scheduling of the callback functions to be called: timeMixed_callback every day of the week at 12:00 and 24:00 time of Rome (GMT+2 with daylight savings time)
    updater.job_queue.run_daily(timeMixed_callback, days=(0, 1, 2, 3, 4, 5, 6), time = time(hour = 10))
    updater.job_queue.run_daily(timeMixed_callback, days=(0, 1, 2, 3, 4, 5, 6), time = time(hour = 22))

    # defining the commands to which the bot will reply and the associated function
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('command', command))
    dispatcher.add_handler(CommandHandler('time', timeMixed_command))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    sys.exit()

if __name__ == '__main__':
    main()
