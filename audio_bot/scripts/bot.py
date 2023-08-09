import audio
import telebot
import os.path
import logging
import langdetect
from gtts import gTTS
from telebot import types

token = 'your_token'
bot = telebot.TeleBot(token)
DESCRIPTION = 'This bot can convert voice messages to text, convert sent '\
              'audio file to text or sent text to audio file and send the '\
              'result to mail or chat'
HELP = 'I can help you with audio (🎙️ ➞ 📃 or 📃 ➞ 🎙️):\n' \
       '\nIf you send a voice message, the bot will convert it to text'\
       '\nIf you send an audio file or video, the bot will convert it to text'\
       '\nIf you send a text, the bot will convert it to an audio file ️'
text_of_the_previous_message = ' '


if __name__ == '__main__':
    pass


def logger_initialization():
    py_logger_init = logging.getLogger("audio_bot")
    py_logger_init.setLevel(logging.WARNING)

    date_fmt = "%Y-%m-%d %H:%M:%S"
    str_fmt = "%(asctime)s : [%(levelname)s] : %(name)s : %(message)s"

    py_handler = logging.FileHandler(f"../../audio_bot.log", mode="a",
                                     encoding="utf8")
    py_formatter = logging.Formatter(fmt=str_fmt, datefmt=date_fmt)

    py_handler.setFormatter(py_formatter)
    py_logger_init.addHandler(py_handler)

    return py_logger_init


py_logger = logger_initialization()


@bot.message_handler(commands=['start'])
def start(message):
    first_name = message.from_user.first_name
    name = f', {first_name}' if first_name is not None else ''
    bot.send_message(message.chat.id, f"Hello{name}. "
                                      f"\n{DESCRIPTION}\n\n{HELP}")


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(content_types=['photo', 'sticker', 'location', 'contact',
                                    'new_chat_members', 'left_chat_member',
                                    'new_chat_title', 'new_chat_photo',
                                    'delete_chat_photo', 'group_chat_created',
                                    'supergroup_chat_created', 'channel_chat_created',
                                    'migrate_to_chat_id', 'migrate_from_chat_id',
                                    'pinned_message', 'web_app_data'])
def help_any_content_type(message):
    help_command(message)


@bot.message_handler(content_types=['voice'])
def convert_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    result = audio.convert_to_text(file_info, token)

    bot.reply_to(message, result)


@bot.message_handler(content_types=['text'])
def convert_text(message):
    global text_of_the_previous_message

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Cancel text to audio file conversion',
                                          callback_data='cancel'))
    markup.add(types.InlineKeyboardButton('Convert text to audio',
                                          callback_data='convert_text_to_audio'))

    text_of_the_previous_message = message.text
    bot.reply_to(message, 'Select an action', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_functions(callback):
    match callback.data:
        case 'cancel':
            help_command(callback.message)
        case 'convert_text_to_audio':
            convert_text_to_audio(callback.message)


def convert_text_to_audio(message):
    try:
        text = text_of_the_previous_message
        detect_language = langdetect.detect(text)
        my_obj = gTTS(text=text, lang=detect_language, slow=False)
        file_name = f'{message.chat.id}.mp3'
        my_obj.save(file_name)
        with open(file_name, 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file)
    except ValueError:
        py_logger.warning("Language incompatibility", exc_info=True)
        bot.send_message(message.chat.id, 'Change the text of the message or '
                                          'perhaps your language is not '
                                          'supported')
    except IOError:
        py_logger.warning("File input or output error", exc_info=True)
        bot.send_message(message.chat.id, 'Try again')
    finally:
        try:
            os.remove(file_name)
        except UnboundLocalError:
            py_logger.warning("File deletion error", exc_info=True)


@bot.message_handler(content_types=['audio', 'document', 'video', 'video_note'])
def convert_to_text(message):

    file_info = bot.get_file((None if message.audio is None else message.audio.file_id)
                             or (None if message.document is None else message.document.file_id)
                             or (None if message.video is None else message.video.file_id)
                             or (None if message.video_note is None else message.video_note.file_id))

    result = audio.convert_to_text(file_info, token)

    bot.reply_to(message, result)


bot.polling(none_stop=True)
