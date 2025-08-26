from utils import *


@bot.message_handler(commands=["start"])
def send_welcome(message: Message):
    bot.reply_to(message, f"Привіт, {message.chat.first_name}, я ваш розважальний бот-асистент!\nЯк можу допомогти?")


@bot.message_handler(commands=["help"])
def send_help(message: Message):
    bot.reply_to(message, "Я можу відповідати вам в чаті, або виконувати деякі команди. Наприклад, спробуйте /info.")


@bot.message_handler(commands=["info"])
def send_info(message: Message):
    bot.reply_to(message, text_info)


@bot.message_handler(commands=["game"])
def game(message: Message):
    bot.send_message(message.chat.id,
                     "Добре, давай зіграємо, я загадав число від 1 до 100.\nТвоя задача його відгадати.\nСкажи кінець гри, якщо хочешь закінчити гру.")
    correct_numbers[message.chat.id] = random.randint(0, 100)
    bot.send_message(message.chat.id, "ready game")
    bot.register_next_step_handler(message, processing_game)


@bot.message_handler(commands=["weather"])
def weather(message: Message):
    bot.send_message(message.chat.id, "Добре, зараз подивимось...\nВкажи місто, в якому ти хочеш визначити погоду (укр або en)")
    bot.register_next_step_handler(message, get_weather)


@bot.message_handler(commands=["currency"])
def currency_command(message: Message):
    bot.send_message(message.chat.id, "Добре, вкажи суму")
    bot.register_next_step_handler(message, currency_exchange)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != "else":
        amount = amounts[call.message.chat.id]
        values = call.data.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"Ви отримаєте: {round(res, 2)}")
        return
    else:
        bot.send_message(call.message.chat.id, "Вкажіть пару валют разділених /")
        bot.register_next_step_handler(call.message, my_currency_exchange)


# Функція штучного асистента для текстових повідомлень
@bot.message_handler(content_types=["text"])
def assistant_response(message: Message):
    user_text = message.text.lower()
    text_commands(user_text, message)


# Запуск бота
bot.infinity_polling()
