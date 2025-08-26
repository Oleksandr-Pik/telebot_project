import os
import json
from config import bot
from functions import *
from dotenv import load_dotenv
from currency_converter import CurrencyConverter
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
WEATHER_API = os.environ.get("WEATHER_API")
amounts = {}
correct_numbers = {}
currency = CurrencyConverter()

text_info = """Бот створений на базі бібліотеки pyTelegramBotAPI, щоб допомагати вам!\n
Даний бот може відповідати вам в чаті 💬, 
📖 рекомендувати книги, 🎵 музику, 
🕹️ грати з вами в ігри /game, 
🤣 розказати анекдот,
🕓 підказати час, 
згенерувати випадкове число від 1 до 100,
🪙 зімітувати підкидання монети,  
💵 отримати поточний курс долара💲,
або ж скористатися конвертером валют /currency,
☁️ 🌡️ отримати інформацію про погоду /weather.
"""


def text_commands(user_text, message):
    for phrase in data:
        for input_words in phrase["input"]:
            if input_words in user_text.lower():
                output = random.choice(phrase["output"])
                function_name = phrase.get("function")
                if function_name:
                    func = globals().get(function_name)
                    if func:
                        output_func = func(user_text)
                        for key in output_func.keys():
                            output = output.replace(f"[{key}]", str(output_func[key]))

                bot.reply_to(message, output)
                return
    variants = [
        "Я тебе не розумію",
        "Мене ще не навчили цьому",
        "Я ще не знаю таку команду",
        "Це дуже цікаво, але я навіть не знаю що тобі відповісти",
        "Хм...\nСпробуй написати щось інше"
    ]
    bot.reply_to(message, random.choice(variants))
    return


def processing_game(message: Message):
    text = message.text
    bot.reply_to(message, f"Ви сказали: {message.text}")
    correct_number = correct_numbers[message.chat.id]
    if text.isdigit():
        number_user = int(text)
        if number_user == correct_number:
            bot.reply_to(message, "Вітаю ти вгадав!\nМожемо зіграти ще, якщо захочеш. Ти вже знаєш як почати гру.")
            return
        elif number_user < correct_number:
            bot.reply_to(message, f"Спробуй ще, моє число більше за {number_user}")
            bot.register_next_step_handler(message, processing_game)
        elif number_user > correct_number:
            bot.reply_to(message, f"Спробуй ще, моє число меньше за {number_user}")
            bot.register_next_step_handler(message, processing_game)
    elif "кінець" in text:
        bot.reply_to(message,
                     "Сумно, що ти не хочеш продовжити.\nАле ми можемо зіграти іншого рзу, якщо захочеш. Ти вже знаєш як почати гру.")
        return
    else:
        bot.reply_to(message, "Напиши тільки число і нічого зайвого")
        bot.register_next_step_handler(message, processing_game)


def get_weather(message: Message):
    bot.reply_to(message, f"Ви сказали: {message.text}\nВже посилаю запит, треба трохи почекати...")
    city = message.text.strip().lower()
    try:
        res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric")
        data = json.loads(res.text)
        bot.reply_to(message,
                     f"Зараз погода:\nТемпература повітря 🌡️ {data["main"]["temp"]}℃\nВологість {data["main"]["humidity"]}%\nШвидкість вітру 💨 {data["wind"]["speed"]}м/с\n{data["weather"][0]["description"]}")
    except KeyError:
        bot.reply_to(message, "Щось пішло не так...\nСпробуй ще раз вказати місто.")
        bot.register_next_step_handler(message, get_weather)


def currency_exchange(message: Message):
    try:
        amounts[message.chat.id] = int(message.text.strip())
        amount = amounts[message.chat.id]
    except ValueError:
        bot.send_message(message.chat.id, "Невірний формат, вкажіть суму")
        bot.register_next_step_handler(message, currency_exchange)
        return
    if amount > 0:
        markup = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton("USD/EUR", callback_data="USD/EUR")
        btn2 = InlineKeyboardButton("EUR/USD", callback_data="EUR/USD")
        btn3 = InlineKeyboardButton("USD/GBP", callback_data="USD/GBP")
        btn4 = InlineKeyboardButton("Інша пара", callback_data="else")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Оберіть пару валют", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Число має бути більше за 0.\nВкажіть суму")
        bot.register_next_step_handler(message, currency_exchange)


def my_currency_exchange(message: Message):
    try:
        amount = amounts[message.chat.id]
        values = message.text.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f"Ви отримаєте: {round(res, 2)}")
        return
    except Exception:
        bot.send_message(message.chat.id, "Щось пішло не так.\nВкажіть ще раз пару валют через /")
        bot.register_next_step_handler(message, my_currency_exchange)


def load_speech():
    with open("speech.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


data = load_speech()
