import random

from datetime import timedelta
from time import time
from telebot import types

import SQL_helpers
from main_classes import Sneakers, Sneaker


def make_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    get_new_sneakersButton = types.KeyboardButton("👟 Get sneakers")
    get_my_sneakersButton = types.KeyboardButton("🗂 My sneakers")
    get_sneaker_houseButton = types.KeyboardButton("🏠 Sneakers house")

    markup.row(get_new_sneakersButton, get_my_sneakersButton)
    markup.row(get_sneaker_houseButton)

    return markup


def send_start_message(bot, message, markup):
    text = f"""
    <b>🫱🏿 Welcome {message.from_user.first_name} 🫲🏻</b>\n
SoleHunt Bot: Your gateway to sneaker paradise! \n
Join the ultimate sneaker community where you can hunt down coveted kicks, showcase your collection, and earn ratings from fellow enthusiasts. \n
Dive into the exhilarating world of sneaker culture and elevate your style with every step. \n
Ready to lace up and level up? Get started with SoleHunt now!"""

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")


def display_time_until_next_attempt(user, bot, message):
    time_left_in_sec = 14400 - (time() - user.user_last_button_press_timer)
    time_left = timedelta(seconds=time_left_in_sec)
    formatted_time = str(time_left).split('.')[0]

    bot.send_message(message.chat.id, f"⏳Wait {formatted_time} before next attempt")


def update_time_until_next_attempt(user):
    user.user_last_button_press_timer = time()


def send_received_sneakers_and_update_user_rating(user, bot, message):
    sneaker_id, name, image, type_, rarity, price, heat = get_random_sneakers_and_update_user_sneakers(user)
    image = get_image_data(image)
    user.user_rating += heat

    bot.send_photo(
        message.chat.id,
        image,
        caption=f"Here's your sneakers:   \n\n✨{name} '{type_}' - {price}€\n🎃Rarity - {rarity}\n🔥Heat - {heat}"
                f"\n\nYour rating got increased by {heat}🔥"
                f"\n\nPlease visit us in 4 hours for your next try 😉"
    )


def get_random_sneakers_and_update_user_sneakers(user):
    sneakers = Sneakers(get_random_sneaker_rarity()).get_sneakers_by_rarity()
    sneaker = random.choice(sneakers)
    sneaker_id, *_ = sneaker
    user.add_sneaker_to_user_sneakers(sneaker_id)

    return sneaker


def get_random_sneaker_rarity():
    rarity_probabilities = {
        "common": 55,
        "rare": 30,
        "very rare": 10,
        "ultra rare": 4.5,
        "grail": 0.49999,
        "unknown": 0.00001
    }

    chosen_rarity = random.choices(
        list(rarity_probabilities.keys()),
        list(rarity_probabilities.values())
    )[0]

    return chosen_rarity


def get_image_data(image):
    image_path = f"images/{image}"
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    return image_data


def display_user_sneakers_or_display_error_message(user, bot, message):
    user_sneakers = get_user_sneakers(user)

    if user_sneakers:
        show_sneakers(bot, message, 0, len(user_sneakers) - 1, user_sneakers)
    else:
        bot.send_message(message.chat.id, "😓 You dont have any sneakers yet")


def get_user_sneakers(user):
    user_sneakers = user.get_user_sneakers()
    user_sneakers = [Sneaker(sneaker_id) for sneaker_id, in user_sneakers]

    return user_sneakers


def show_sneakers(bot, message, start_index, end_index, user_sneakers):
    sneaker = user_sneakers[start_index]
    name, image, type_, rarity, price, heat = sneaker.sneaker_name, sneaker.sneaker_image, sneaker.sneaker_type, sneaker.sneaker_rarity, sneaker.sneaker_price, sneaker.sneaker_heat
    image = get_image_data(image)

    markup = make_show_sneakers_markup(start_index, end_index)

    bot.send_photo(
        message.chat.id,
        image,
        caption=f"✨{name} '{type_}' - {price}€\n🎃Rarity - {rarity}\nStrength(heat) - {heat}🔥",
        reply_markup=markup
    )


def make_show_sneakers_markup(start_index, end_index):
    markup = types.InlineKeyboardMarkup()

    previous_sneakersButton = types.InlineKeyboardButton("⬅️", callback_data=f"prev_sneakers:{start_index}:{end_index}")
    index_of_sneakersButton = types.InlineKeyboardButton(f"#{start_index + 1}/{end_index + 1}", callback_data=" ")
    next_sneakersButton = types.InlineKeyboardButton("➡️", callback_data=f"next_sneakers:{start_index}:{end_index}")

    markup.row(previous_sneakersButton, index_of_sneakersButton, next_sneakersButton)

    return markup


def make_sneakers_house_menu_markup():
    markup = types.InlineKeyboardMarkup()

    get_ratingButton = types.InlineKeyboardButton("🥇 Rating", callback_data="get_rating")
    get_global_ratingButton = types.InlineKeyboardButton("🏆 Global rating", callback_data="get_global_rating")
    enter_promo_codeButton = types.InlineKeyboardButton("🎁 Enter promo-code", callback_data="enter_promo_code")

    markup.row(get_ratingButton, get_global_ratingButton)
    markup.row(enter_promo_codeButton)

    return markup


def define_user_league(user):
    user_rating = user.user_rating
    print(user_rating)

    leagues = {
        range(100, 500): "wood",
        range(500, 2000): "stone",
        range(2000, 5000): "bronze",
        range(5000, 10000): "silver",
        range(10000, 20000): "gold",
        range(20000, 50000): "crystal",
        range(50000, 100_000): "elite",
        range(100_000, 1_000_000): "champion",
        range(1_000_000, 10_000_000): "legend",
        range(10_000_000, 100_000_000): "?"
    }

    for key in leagues:
        if user_rating in key:
            user.user_league = leagues[key]

    print(user.user_league)


def get_topn_rating(bot, message, n):
    query = "SELECT user_id, user_rating, user_league FROM users ORDER BY user_rating DESC LIMIT ?;"
    params = (n, )

    ratings = SQL_helpers.SQLCommandor().sql_select(query, params)
    text = "place. name - rating - league\n\n"
    for place, ratings in enumerate(ratings, 1):
        user_id, rating, league = ratings
        first_name = bot.get_chat_member(user_id, user_id).user.first_name
        match place:
            case 1:
                text += f"🥇{place}. {first_name} - {rating} - {league}\n"
            case 2:
                text += f"🥈{place}. {first_name} - {rating} - {league}\n"
            case 3:
                text += f"🥉{place}. {first_name} - {rating} - {league}\n"
            case _:
                text += f"{place}. {first_name} - {rating} - {league}\n"

    bot.send_message(message.chat.id, text)


def verify_promo_code(message, user, bot):
    promo_code = message.text
    try:
        related_sneaker_id = Sneakers(promo_code=promo_code).get_sneaker_id_by_promo_code()

        if related_sneaker_id:
            Sneakers(promo_code=promo_code).delete_used_promo_code()
            promo_sneaker = Sneaker(related_sneaker_id)
            define_user_league(user)
            send_received_promo_sneaker_and_update_user_rating(user, bot, message, promo_sneaker)
        else:
            bot.reply_to(message, "🤨 Wrong promo-code or promo-code is already used.")
    except IndexError:
        bot.reply_to(message, "🤨 Wrong promo-code or promo-code is already used.")


def send_received_promo_sneaker_and_update_user_rating(user, bot, message, promo_sneaker):
    sneaker_id, name, image, type_, rarity, price, heat = promo_sneaker.sneaker_id, promo_sneaker.sneaker_name, promo_sneaker.sneaker_image, promo_sneaker.sneaker_type, promo_sneaker.sneaker_rarity, promo_sneaker.sneaker_price, promo_sneaker.sneaker_heat
    image = get_image_data(image)

    user.add_sneaker_to_user_sneakers(sneaker_id)
    user.user_rating += heat

    bot.send_photo(
        message.chat.id,
        image,
        caption=f"Here's your promo-sneakers 🥸\n\n✨{name} '{type_}' - {price}€\n🎃Rarity - {rarity}\nStrength(heat) - {heat}🔥"
    )
