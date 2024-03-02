from SQL_helpers import SQLCommandor


class User:
    def __init__(self, user_id, user_rating=0, user_league='wooden', user_last_button_press_timer=0):
        self.__user_id = user_id
        self.__user_rating = user_rating
        self.__user_league = user_league
        self.__user_last_button_press_timer = user_last_button_press_timer
        self.__create_user()

    def __create_user(self):
        query = """
        INSERT INTO users (user_id, user_rating, user_league, user_last_button_press_timer)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM users WHERE user_id = ?
        )
        """
        params = (
            self.__user_id, self.__user_rating, self.__user_league, self.__user_last_button_press_timer, self.__user_id)

        SQLCommandor().sql_insert(query, params)

    def get_user_sneakers(self):
        query = """
        SELECT related_sneaker FROM user_sneakers WHERE related_user = ?
        """
        params = (self.user_id,)

        return SQLCommandor().sql_select(query, params)

    def add_sneaker_to_user_sneakers(self, sneaker_id):
        query = """
        INSERT INTO user_sneakers (related_user, related_sneaker) VALUES (?, ?)
        """
        params = (self.user_id, sneaker_id)

        SQLCommandor().sql_insert(query, params)

    def get_user_rating(self):
        query = """
        SELECT user_rating FROM users WHERE user_id = ?
        """
        params = (self.__user_id,)

        user_rating, = SQLCommandor().sql_select(query, params)[0]
        return user_rating

    def get_user_league(self):
        query = """
        SELECT user_league FROM users WHERE user_id = ?
        """
        params = (self.__user_id,)

        user_league, = SQLCommandor().sql_select(query, params)[0]
        return user_league

    def get_user_last_button_press_timer(self):
        query = """
        SELECT user_last_button_press_timer FROM users WHERE user_id = ?
        """
        params = (self.__user_id,)

        user_last_button_press_timer, = SQLCommandor().sql_select(query, params)[0]
        return user_last_button_press_timer

    def set_user_rating(self, new_rating):
        query = """
        UPDATE users SET user_rating = ? WHERE user_id = ?
        """
        params = (new_rating, self.__user_id)

        SQLCommandor().sql_update(query, params)
        self.__user_rating = new_rating

    def set_user_league(self, new_league):
        query = """
        UPDATE users SET user_league = ? WHERE user_id = ?
        """
        params = (new_league, self.__user_id)

        SQLCommandor().sql_update(query, params)
        self.__user_league = new_league

    def set_user_last_button_press_timer(self, new_last_button_press_timer):
        query = """
        UPDATE users SET user_last_button_press_timer = ? WHERE user_id = ?
        """
        params = (new_last_button_press_timer, self.__user_id)

        SQLCommandor().sql_update(query, params)
        self.__user_last_button_press_timer = new_last_button_press_timer

    @property
    def user_id(self):
        return self.__user_id

    @property
    def user_rating(self):
        return self.__user_rating

    @property
    def user_league(self):
        return self.__user_league

    @property
    def user_last_button_press_timer(self):
        return self.__user_last_button_press_timer

    @user_rating.setter
    def user_rating(self, value):
        self.set_user_rating(value)

    @user_league.setter
    def user_league(self, value):
        self.set_user_league(value)

    @user_last_button_press_timer.setter
    def user_last_button_press_timer(self, value):
        self.set_user_last_button_press_timer(value)


class Sneaker:
    def __init__(self, sneaker_id):
        self.__sneaker_id = sneaker_id
        self.__sneaker_name = None
        self.__sneaker_image = None
        self.__sneaker_type = None
        self.__sneaker_rarity = None
        self.__sneaker_price = None
        self.__sneaker_heat = None
        self.__fill_sneaker_info()

    def __fill_sneaker_info(self):
        query = """
        SELECT name, image, type, rarity, price, heat FROM sneakers WHERE id = ?
        """
        params = (self.sneaker_id,)

        (self.__sneaker_name,
         self.__sneaker_image,
         self.__sneaker_type,
         self.__sneaker_rarity,
         self.__sneaker_price,
         self.__sneaker_heat) = SQLCommandor().sql_select(query, params)[0]

    @property
    def sneaker_id(self):
        return self.__sneaker_id

    @property
    def sneaker_name(self):
        return self.__sneaker_name

    @property
    def sneaker_image(self):
        return self.__sneaker_image

    @property
    def sneaker_type(self):
        return self.__sneaker_type

    @property
    def sneaker_rarity(self):
        return self.__sneaker_rarity

    @property
    def sneaker_price(self):
        return self.__sneaker_price

    @property
    def sneaker_heat(self):
        return self.__sneaker_heat


class Sneakers:
    def __init__(self, rarity=None, promo_code=None):
        self.__rarity = rarity
        self.__promo_code = promo_code

    def get_sneakers_by_rarity(self):
        query = """
        SELECT * FROM sneakers WHERE rarity = ?
        """
        params = (self.__rarity,)
        queryset = SQLCommandor().sql_select(query, params)
        return queryset

    def get_sneaker_id_by_promo_code(self):
        query = """
        SELECT related_sneaker FROM promo_sneakers WHERE promo_code = ?
        """
        params = (self.__promo_code,)

        related_sneaker_id, = SQLCommandor().sql_select(query, params)[0]

        return related_sneaker_id

    def delete_used_promo_code(self):
        query = """
        DELETE FROM promo_sneakers WHERE promo_code = ?
        """
        params = (self.__promo_code,)

        SQLCommandor().sql_delete(query, params)
