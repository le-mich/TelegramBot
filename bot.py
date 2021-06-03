import logging, sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, Defaults
from datetime import time, datetime
from pytz import timezone

# import API handler
from api import API, SAVED_APIS

# import imdb database and initialize object
import imdb
ia = imdb.IMDb()

# import sensitive elements from separated python document
from instanceElements import TK as TOKEN
from instanceElements import GID as GROUPID

# init chat stages
FILM, DATE, MAGNET = range(3)


### Help function
def help(update, context):
    context.bot.sendMessage(chat_id=update.effective_chat.id, text="""/orario - invia l'orario
/di - fa dire qualcosa ad Elsa
/aggiungiFilm - avvia una chat per programmare un film
/imdb - manda il link di imdb del film cercato
/aiuto - mostra questo messaggio""")


### Time functions

# content factory
def timeMixed_content():
    time = datetime.now().strftime("%A %d/%m/%y, %H:%M")
    apiResult = apiHandler.callRandomEndpoint()
    return "{}\n{}".format(time, apiResult)

# base function
def timeMixed(context, chat=GROUPID):
    context.bot.sendMessage(chat_id=chat, text=timeMixed_content())

# command and callback
def timeMixed_command(update, context):
    timeMixed(context, chat=update.effective_chat.id)

def timeMixed_callback(context: CallbackContext):
    timeMixed(context)


### API functions

def cache_callback(context: CallbackContext):
    apiHandler.populateCache()


### "say" function
def say(update, context, chat=GROUPID):
    phrase = update.message.text.replace('/di ', '')
    context.bot.sendMessage(chat_id=chat, text=phrase)

### IMDB url functions
def imdbFilm(update, context):
    movies = ia.search_movie(update.message.text.replace('/imdb ', ''))
    context.bot.sendMessage(chat_id=update.effective_chat.id, text='Miglior match:\nhttps://www.imdb.com/title/tt{}'.format(movies[0].movieID))


### Film functions
# callable command
def addFilm(update, context):
    chat_id = update.message.chat.id
    context.bot.sendMessage(chat_id=chat_id, text='Vuoi aggiungere un nuovo film al calendario. Che film vuoi aggiungere?')

    return FILM

# chatbot stage one
def insertFilm(update, context):
    film = update.message.text
    chat_id = update.message.chat.id

    context.bot_data['film'] = film
    context.bot.send_message(chat_id=chat_id, text='Ok vuoi vedere {}. In che data? **(dd-mm-yyyy)**'.format(film))

    return DATE

# stage two
def insertDate(update, context):
    global updater

    date = update.message.text
    film = context.bot_data['film']

    chat_id = update.message.chat.id

    context.bot_data['date'] = date

    context.bot.sendMessage(chat_id=chat_id, text='Ho impostato un reminder per *{}* il {}! Se vuoi puoi mandare un magnet per il download, altrimenti invia "Done".'.format(film, date))

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

    updater.job_queue.run_once(film_callback, converted_date, context=temp)

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

    context.bot.sendMessage(chat_id=chat_id, text=text_message)


### Fallback functions
# unknown command
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Wut?')

# conversation fallback
def fallback(context, update):
    context.bot.sendMessage(chat_id=chat_id, text='Deve esserci stato un errore, riprova.')

    return ConversationHandler.END


def main():
    global updater
    global apiHandler

    defaults = Defaults(tzinfo=timezone('Europe/Rome'), parse_mode='Markdown')
    updater = Updater(TOKEN, defaults=defaults, use_context=True)
    dispatcher = updater.dispatcher

    # Load saved apis
    apiHandler = API(SAVED_APIS)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # scheduling of the callback functions to be called: timeMixed_callback every day of the week at 12:00 and 24:00 time of Rome (GMT+2 with daylight savings time)
    updater.job_queue.run_daily(cache_callback, time=time(hour=16,minute=45))
    updater.job_queue.run_daily(timeMixed_callback, time=time(hour=12))
    updater.job_queue.run_daily(timeMixed_callback, time=time(hour=0))

    # setting up film handler
    film_handler = ConversationHandler(
        entry_points = [CommandHandler('aggiungiFilm', addFilm)],

        states = {
            FILM: [MessageHandler(Filters.text, insertFilm)],
            DATE: [MessageHandler(Filters.text, insertDate)],
            MAGNET: [MessageHandler(Filters.text, insertMagnet)]
        },

        fallbacks = [MessageHandler(Filters.text, fallback)],
        per_user = False
    )

    # defining the commands to which the bot will reply and the associated function
    dispatcher.add_handler(film_handler)
    dispatcher.add_handler(CommandHandler('di', say))
    dispatcher.add_handler(CommandHandler('imdb', imdbFilm))
    dispatcher.add_handler(CommandHandler('aiuto', help))
    dispatcher.add_handler(CommandHandler('orario', timeMixed_command))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()
    sys.exit()

if __name__ == '__main__':
    main()
