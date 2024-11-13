import telebot
import random

TOKEN = '7239325544:AAEN0n-YvJw9KjRQh_tKIyne8uweCWw4fZY'
bot = telebot.TeleBot(TOKEN)

user_message_count = {}

sticker_pool = [
    {'id': 'CAACAgIAAxkBAAEKBipnNNygwiU3FN0v0P_6EI55Zo4dywACZFoAAjUoIUn5izprfvq-PzYE', 'chance': 0.5, 'message': 'Выпал обычный-чиназес стикер'},
    {'id': 'CAACAgIAAxkBAAEKBixnNNypO81BBj8-biUn83WeJw6zDwACoVcAApbiKUmvO0oITRkKwzYE', 'chance': 0.3, 'message': 'Выпал редкий-чиназес стикер'},
    {'id': 'CAACAgIAAxkBAAEKBi5nNNyxFGD6O2DxB-wB_JS-_PMK8QAC4lsAAqPzIEkB-jrX-WEbmTYE', 'chance': 0.2, 'message': 'Выпал эпический-чиназес стикер'},
    {'id': 'CAACAgIAAxkBAAEKBltnNORkleFup2N952IITKNSjBwmdQACC1cAAjXcKUnKxRuqq1W1tDYE', 'chance': 0.7, 'message': 'Вам выпал хуевый стикер'}
]

def choose_sticker():
    random_value = random.random()
    cumulative_probability = 0.0
    for sticker in sticker_pool:
        cumulative_probability += sticker['chance']
        if random_value <= cumulative_probability:
            return sticker
    return sticker_pool[-1]

@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
def track_user_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in user_message_count:
        user_message_count[chat_id] = {}

    if user_id not in user_message_count[chat_id]:
        user_message_count[chat_id][user_id] = 0

    user_message_count[chat_id][user_id] += 1

    if user_message_count[chat_id][user_id] == 10:
        user_message_count[chat_id][user_id] = 0

        chosen_sticker = choose_sticker()
        bot.send_sticker(chat_id, chosen_sticker['id'])
        bot.send_message(chat_id, f"{chosen_sticker['message']} (Шанс: {chosen_sticker['chance'] * 100:.0f}%)")

bot.polling(none_stop=True)