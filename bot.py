import logging, sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from datetime import time, datetime

# import sensitive elements from separated python document
from instanceElements import TK as TOKEN
from instanceElements import GID as GROUPID

# init chat stages
FILM, DATE, MAGNET = range(3)


### Help function
def help(update, context):
    context.bot.sendMessage(chat_id=update.effective_chat.id, text="""/time - invia l'orario
/addFilm - avvia una chat per programmare un film
/help - mostra questo messaggio""")


### Time functions
# base function
def timeMixed(context, chat = GROUPID):
    context.bot.sendMessage(chat_id = chat, text = datetime.now().strftime("%A %d/%m/%y, %H:%M"))

# command and callback
def timeMixed_command(update, context):
    timeMixed(context, chat = update.effective_chat.id)

def timeMixed_callback(context: CallbackContext):
    timeMixed(context)


### Film functions
# callable command
def addFilm(update, context):
    chat_id = update.message.chat.id
    context.bot.sendMessage(chat_id = chat_id, text='Vuoi aggiungere un nuovo film al calendario. Che film vuoi aggiungere?', parse_mode='Markdown')

    return FILM

# chatbot stage one
def insertFilm(update, context):
    film = update.message.text
    chat_id = update.message.chat.id

    context.bot_data['film'] = film
    context.bot.send_message(chat_id = chat_id, text = 'Ok vuoi vedere {}. In che data? **(dd-mm-yyyy)**'.format(film), parse_mode='Markdown')

    return DATE

# stage two
def insertDate(update, context):
    global updater

    date = update.message.text
    film = context.bot_data['film']

    chat_id = update.message.chat.id

    context.bot_data['date'] = date

    context.bot.sendMessage(chat_id = chat_id, text = 'Ho impostato un reminder per *{}* il {}! Se vuoi puoi mandare un magnet per il download, altrimenti invia "Done".'.format(film, date), parse_mode = 'Markdown')

    return MAGNET

def insertMagnet(update, context):

    temp = dict()

    chat_id = update.message.chat.id
    magnet = update.message.text

    temp['date'] = context.bot_data['date']
    temp['film'] = context.bot_data['film']
    temp['chat'] = chat_id
    temp['magnet'] = magnet

    converted_date = datetime.strptime(date, '%d-%m-%Y')

    updater.job_queue.run_once(film_callback, converted_date, context = temp)

    return ConversationHandler.END

# callback function
def film_callback(context):
    chat_id = context.job.context['chat']
    film = context.job.context['film']
    magnet = context.job.context['magnet']

    if magnet == 'Done':
        text_message = '*Reminder*: oggi dovete guardare {}'.format(film)
    else:
        text_message = '*Reminder*: oggi dovete guardare {}. Potete scaricare il film da [qui]({}) '.format(film, magnet)

    context.bot.sendMessage(chat_id = chat_id, text = text_message, parse_mode = 'Markdown')


### Fallback functions
# unknown command
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Wut?')

# conversation fallback
def fallback(context, update):
    context.bot.sendMessage(chat_id = chat_id, text = 'Deve esserci stato un errore, riprova.', parse_mode = 'Markdown')

    return ConversationHandler.END


def main():
    global updater

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # scheduling of the callback functions to be called: timeMixed_callback every day of the week at 12:00 and 24:00 time of Rome (GMT+2 with daylight savings time)
    updater.job_queue.run_daily(timeMixed_callback, days=(0, 1, 2, 3, 4, 5, 6), time = time(hour = 11))
    updater.job_queue.run_daily(timeMixed_callback, days=(0, 1, 2, 3, 4, 5, 6), time = time(hour = 23))

    # setting up film handler
    film_handler = ConversationHandler(
        entry_points = [CommandHandler('addfilm', addFilm)],

        states = {
            FILM: [MessageHandler(Filters.text, insertFilm)],
            DATE: [MessageHandler(Filters.text, insertDate)],
            MAGNET : [MessageHandler(Filters.text, insertMagnet)]
        },

        fallbacks = [MessageHandler(Filters.text, fallback)],
        per_user = False
    )

    # defining the commands to which the bot will reply and the associated function
    dispatcher.add_handler(film_handler)
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('time', timeMixed_command))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()
    sys.exit()

if __name__ == '__main__':
    main()
