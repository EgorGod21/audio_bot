# TELEGRAM AUDIO BOT #

<p>This telegram bot can make your life much easier.

Bot can:
1. Convert audio messages, video notes, video files, audio files to text;
2. Convert text to audio file.
</p>

## STARTING THE AUDIO BOT ##

In the script at the address `audio_bot/scripts/bot.py`
```python
token = 'your_token'
```
variable `token` needs to be assigned the token of your telegram bot, which can be created by [the link](https://t.me/BotFather).

In the script at the address `audio_bot/scripts/audio.py`
```python
openai.api_key = 'your_api_key'
```
variable `openai.api_key` needs to be assigned your [API key](https://platform.openai.com/account/api-keys), to get the API key you need to register.
You can read [API documentation](https://platform.openai.com/docs/introduction).

Project logs will be kept in file `audio_bot.log`.