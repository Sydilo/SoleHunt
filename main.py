from telebot import TeleBot

from main_classes import User
from utils import *

bot = TeleBot("6976249671:AAHEb4zHfoxjItrI2HobSZ_I79bmxWl5Kfw")
user = None


@bot.message_handler(commands=["start"])
def start(message):
    global user
    user = User(message.from_user.id)
    markup = make_main_markup()
    send_start_message(bot, message, markup)


@bot.message_handler(func=lambda message: message.text == "👟 Get sneakers")
def get_new_sneakers(message):
    if user and user.user_last_button_press_timer and time() - user.user_last_button_press_timer < 5:
        display_time_until_next_attempt(user, bot, message)
    else:
        update_time_until_next_attempt(user)
        send_received_sneakers_and_update_user_rating(user, bot, message)


@bot.message_handler(func=lambda message: message.text == "🗂 My sneakers")
def get_my_sneakers(message):
    display_user_sneakers_or_display_error_message(user, bot, message)


@bot.callback_query_handler(func=lambda call: call.data.startswith("next_sneakers:"))
def display_next_sneakers(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    data = call.data.split(":")
    if int(data[1]) == int(data[2]):
        start_index = 0
        show_sneakers(bot, call.message, start_index, int(data[2]), get_user_sneakers(user))
    else:
        start_index = int(data[1]) + 1
        show_sneakers(bot, call.message, start_index, int(data[2]), get_user_sneakers(user))


@bot.callback_query_handler(func=lambda call: call.data.startswith("prev_sneakers:"))
def display_previous_sneakers(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    data = call.data.split(":")
    if int(data[1]) == 0:
        start_index = int(data[2])
        show_sneakers(bot, call.message, start_index, int(data[2]), get_user_sneakers(user))
    else:
        start_index = int(data[1]) - 1
        show_sneakers(bot, call.message, start_index, int(data[2]), get_user_sneakers(user))


@bot.message_handler(func=lambda message: message.text == "🏠 Sneakers house")
def get_sneakers_house_menu(message):
    markup = make_sneakers_house_menu_markup()

    bot.reply_to(message, "Choose an action:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "get_rating")
def get_rating(call):
    define_user_league_and_return(user, bot, call.message)


@bot.callback_query_handler(func=lambda call: call.data == "enter_promo_code")
def enter_promo_code(call):
    bot.send_message(call.message.chat.id, "⌨️ Enter a promo-code:")


@bot.message_handler(func=lambda message: True)
def promo_code(message):
    verify_promo_code(user, bot, message)


if __name__ == "__main__":
    bot.polling(none_stop=True)
