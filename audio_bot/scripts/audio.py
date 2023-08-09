import os
import bot
import openai
import requests


openai.api_key = 'your_api_key'
IOERROR_TEXT = 'An error has occurred. Try again'
py_logger = bot.logger_initialization()


def return_text_from_audio(file_name):
    try:
        with open(file_name, 'rb') as audio_file:
            transcription = openai.Audio.transcribe(model="whisper-1",
                                                    file=audio_file,
                                                    response_format="text")
        return transcription
    except IOError:
        py_logger.warning("File input or output error", exc_info=True)
        return


def convert_to_text(file_info, token):
    try:
        path = file_info.file_path
        file_name = os.path.basename(path)

        doc = requests.get(f'https://api.telegram.org/file/bot{token}/'
                           f'{file_info.file_path}')

        with open(file_name, 'wb') as f:
            f.write(doc.content)

        text = return_text_from_audio(file_name)
        result = text if text != 'None' else 'Send the voice again'

        return result

    except IOError:
        py_logger.warning("File input or output error", exc_info=True)
        return IOERROR_TEXT
    except openai.error.InvalidRequestError:
        py_logger.warning("This format is not supported", exc_info=True)
        return 'This format is not supported'
    finally:
        try:
            os.remove(file_name)
        except UnboundLocalError:
            py_logger.warning("File deletion error", exc_info=True)
            return IOERROR_TEXT
