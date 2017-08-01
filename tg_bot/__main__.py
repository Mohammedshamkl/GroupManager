import logging
from pprint import pprint

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from tg_bot.config import Development as Configuration
from tg_bot.custom_filters import SimaoFilter
from tg_bot.sql import add_note_to_db, get_note, rm_note


def test(bot, update):
    # pprint(eval(str(update)))
    update.effective_message.reply_text("Hola tester")


def save(bot, update, args):
    chat_id = update.effective_chat.id
    if len(args) >= 2:
        notename = args[0]
        del args[0]
        note_data = " ".join(args)

        add_note_to_db(chat_id, notename, note_data)
        update.effective_message.reply_text("yas! added " + notename)
    else:
        update.effective_message.reply_text("Dude, theres no note")


def get(bot, update, args):
    chat_id = update.effective_chat.id
    if len(args) >= 1:
        notename = args[0]

        note = get_note(chat_id, notename)
        if note:
            update.effective_message.reply_text(note.value)
            return
        else:
            update.effective_message.reply_text("This doesn't exist")
    else:
        update.effective_message.reply_text("Get rekt")


def delete(bot, update, args):
    chat_id = update.effective_chat.id
    notename = args[0]

    rm_note(chat_id, notename)
    update.effective_message.reply_text("Successfully removed note")


def start(bot, update):
    update.effective_message.reply_text("Yo, whadup?")


def reply_simshit(bot, update):
    update.effective_message.reply_text("Did you mean: simshit?")


def del_message(bot, update):
    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id

    res = bot.deleteMessage(chat_id, message_id)
    if res:
        bot.sendMessage(chat_id, "Bitch no stickers", "HTML")
    else:
        bot.sendMessage(chat_id, "Ehhhhh idk why that didn't work, ask Pol", "HTML")


def main():
    updater = Updater(Configuration.API_KEY)
    dispatcher = updater.dispatcher

    # enable logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO)

    LOGGER = logging.getLogger(__name__)

    test_handler = CommandHandler("test", test)
    start_handler = CommandHandler("start", start)
    save_handler = CommandHandler("save", save, pass_args=True)
    get_handler = CommandHandler("get", get, pass_args=True)
    delete_handler = CommandHandler("delete", delete, pass_args=True)
    simao_handler = MessageHandler(Filters.text & SimaoFilter, reply_simshit)
    sticker_handler = MessageHandler((~ Filters.private)
                                     & (Filters.sticker
                                     | Filters.audio
                                     | Filters.document
                                     | Filters.video
                                     | Filters.contact
                                     | Filters.photo
                                     | Filters.voice), del_message)

    dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(save_handler)
    dispatcher.add_handler(get_handler)
    dispatcher.add_handler(delete_handler)
    # dispatcher.add_handler(simao_handler)
    dispatcher.add_handler(sticker_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()