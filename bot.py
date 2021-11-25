import logging

from aiogram import Bot, Dispatcher, executor, types 
from checkword import check_words
from transliterate import to_cyrillic, to_latin

def transliterate(text, to_variant):
    if to_variant == "cyrillic":
        text = to_cyrillic(text)
    elif to_variant == "latin":
        text = to_latin(text)

    return text

API_TOKEN = "2115798290:AAEiIK1EVYrN0OYciK8Dld0N0FUoEDZSDMo"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.reply("fix_words botiga hush kelibsiz")

@dp.message_handler(commands='help')
async def help_user(message: types.Message):
    await message.reply("Botdan foydalanish uchun o'zbekcha so'z yuboring")

@dp.message_handler()
async def check_imlo(message: types.Message):
    words = message.text
    words = transliterate(words,'cyrillic').split()

    # krilga = lambda msg: to_latin(msg) 
    javob = lambda words: to_cyrillic(words) if words.isascii() else to_latin(words)

    words_list = ""
    for word in words:
        result = check_words(word)
        if result['available']:
            response = f"✅{word.capitalize()}\n"
        else:
            print(word.capitalize(),"soz keldimi")
            response = f"❌{word.capitalize()}\n"
            for text in result['matches']:
                response +=f"✅{text.capitalize()}\n"
        words_list+="next word" + response

        

    await message.answer(javob(words_list))

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)