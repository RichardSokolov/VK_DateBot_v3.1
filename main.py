import vk_api
import requests
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from config import user_token, group_token, line
from database import select_seen
from database import *

group_id = 219861432
sticker_id = 103


class VK_DateBot:

    def __init__(self):
        self.vk = vk_api.VkApi(token=group_token)
        self.vk_u = vk_api.VkApi(token=user_token)
        self.longpoll = VkLongPoll(self.vk)
        print("VK DateBot was created")

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7)})

    def send_sticker(self, user_id):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'sticker_id': 103,
                                         'random_id': randrange(10 ** 7)})

    def city_find(self, user_id, city_name):
        city_info = self.vk_u.method('database.getCities', {'access_token': user_token,
                                                'country_id': 1,
                                                'q': f'{city_name}',
                                                'need_all': 0,
                                                'count': 1000})
        dict_1 = city_info
        list_1 = dict_1['items']
        try:
            for i in list_1:
                found_city_name = i.get('title')
                if found_city_name == city_name:
                    found_city_id = i.get('id')
                    return int(found_city_id)
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def user_info(self, user_id, field):
        user_info = self.vk.method('users.get', {'access_token': user_token,
                                                 'user_ids': user_id,
                                                 'fields': 'first_name, last_name, sex, bdate, city'
                                                 })
        if field == 1:
            try:
                for i in user_info:
                    for key, value in i.items():
                        first_name = i.get(r'first_name')
                for i in user_info:
                    for key, value in i.items():
                        last_name = i.get(r'last_name')
            except KeyError:
                self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')
                print("Ошибка получения токена, введите токен в переменную - user_token")
            name = first_name + " " + last_name
            print('Пользователь -', name)
            return name

        elif field == 2:
            try:
                for i in user_info:
                    for key, value in i.items():
                        user_city_p = i.get('city')
            except KeyError:
                self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')
                print("Ошибка получения токена, введите токен в переменную - user_token")
            if user_city_p is not None:
                user_city = str(user_city_p.get('title'))
                user_city_id = str(user_city_p.get('id'))
                print("Город пользователя -", user_city, "id -", user_city_id)
                return [user_city, user_city_id]
            elif user_city_p is None:
                self.write_msg(user_id,
                               'Не смог определить ваш город, пожалуйста заполните профиль, введите ваш город:')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        user_city = event.text
                        user_city_id = self.city_find(user_id, user_city)
                        if user_city_id != '' or user_city_id != None:
                            return [user_city, user_city_id]
                        else:
                            break
                return [user_city, user_city_id]

        elif field == 3:
            try:
                for i in user_info:
                    for key, value in i.items():
                        user_sex_1 = i.get('sex')
            except KeyError:
                self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')
                print("Ошибка получения токена, введите токен в переменную - user_token")
            if user_sex_1 == 2:
                user_sex = 1
                print("Пол для поиска -", user_sex)
                return user_sex
            elif user_sex_1 == 1:
                user_sex = 1
                print("Пол для поиска -", user_sex)
                return user_sex
            elif user_sex_1 is None:
                self.write_msg(user_id, 'Не смог определить ваш пол, пожалуйста выберите свой пол. (1 - мужской, 2 - женский)')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        user_sex = event.text
                        if user_sex == 2:
                            user_sex = 1
                            print("Пол для поиска -", user_sex)
                            return user_sex
                        elif user_sex_1 == 1:
                            user_sex = 1
                            print("Пол для поиска -", user_sex)
                            return user_sex
        elif field == 4:
            try:
                for i in user_info:
                    for key, value in i.items():
                        user_bdate = i.get('bdate')
            except KeyError:
                self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')
                print("Ошибка получения токена, введите токен в переменную - user_token")
            if user_bdate is not None:
                if len(user_bdate) == 3:
                    print(user_bdate)
                    year_now = int(datetime.date.today().year)
                    date_list = user_bdate.split('.')
                    year = int(date_list[2])
                    return year_now - year
                elif len(user_bdate) == 2:
                    self.write_msg(user_id, 'Не смог узнать ваш возраст.')
                    self.write_msg(user_id, 'Введите нижний порог для поиска:')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            type_age = event.text
                            print(type_age)
                            return type_age
            elif user_bdate is None:
                self.write_msg(user_id, 'Не смог узнать ваш возраст.')
                self.write_msg(user_id, 'Введите нижний порог для поиска:')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        type_age = event.text
                        print(type_age)
                        return type_age
        elif field == 5:
            try:
                for i in user_info:
                    for key, value in i.items():
                        user_bdate = i.get('bdate')
            except KeyError:
                self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')
                print("Ошибка получения токена, введите токен в переменную - user_token")
            if user_bdate is not None:
                if len(user_bdate) == 3:
                    print(user_bdate)
                    year_now = int(datetime.date.today().year)
                    date_list = user_bdate.split('.')
                    year = int(date_list[2])
                    return year_now - year
                elif len(user_bdate) == 2:
                    self.write_msg(user_id, 'Не смог узнать ваш возраст.')
                    self.write_msg(user_id, 'Введите верхний порог для поиска:')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            type_age = event.text
                            print(type_age)
                            return type_age
            elif user_bdate is None:
                self.write_msg(user_id, 'Не смог узнать ваш возраст.')
                self.write_msg(user_id, 'Введите верхний порог для поиска:')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        type_age = event.text
                        print(type_age)
                        return type_age

    def find_user(self, user_id, count):
        find_user = self.vk_u.method('users.search', {'access_token': user_token,
                                                      'v': '5.131',
                                                      'sex': self.user_info(user_id, field=3),
                                                      'age_low': self.user_info(user_id, field=4),
                                                      'age_high': self.user_info(user_id, field=5),
                                                      'city': self.user_info(user_id, field=2),
                                                      'fields': 'is_closed, id, first_name, last_name, city',
                                                      'status': '1' or '6',
                                                      'count': count
                                                      })
        # print(find_user)
        dict_1 = find_user
        list_1 = dict_1['items']
        try:
            for person_dict in list_1:
                if person_dict.get('is_closed') == False:
                    first_name_candidate = person_dict.get("first_name")
                    last_name_candidate = person_dict.get("last_name")
                    vk_id_candidate = str(person_dict.get('id'))
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')
            print("Ошибка получения токена, введите токен в переменную - user_token")
        if select_seen(vk_id_candidate) is None or len(select_seen(vk_id_candidate)) < 0:
            print(select_seen(vk_id_candidate))
            vk_link_candidate = 'vk.com/id' + str(person_dict.get('id'))
            print("----------------")
            print(first_name_candidate)
            print("----------------")
            print(vk_id_candidate)
            insert_data_seen_users(vk_id_candidate)
            return [first_name_candidate, last_name_candidate, vk_id_candidate, vk_link_candidate]
            return f'Поиск завершён'
        else:
            print("DEV INFORMATION: Пользователь уже был найден")

    def find_persons(self, user_id, candidate_information):
        self.write_msg(user_id, self.found_person_info(candidate_information))
        self.person_id(candidate_information)
        self.get_photos_id(self.person_id(candidate_information))
        self.send_photo(user_id, 'Фотография номер 1', candidate_information, 1)
        if self.get_photo(self.person_id(candidate_information), 2) is not None:
            self.send_photo(user_id, 'Фотография номер 2', candidate_information, 2)
        else:
            self.write_msg(user_id, f'У пользователя больше нет фотографий')
        if self.get_photo(self.person_id(candidate_information), 3) is not None:
            self.send_photo(user_id, 'Фотография номер 3', candidate_information, 3)
        else:
            self.write_msg(user_id, f'У пользователя больше нет фотографий')

    def get_photos_id(self, user_id):
        get_photos_id = self.vk_u.method('photos.getAll', {'access_token': user_token,
                                                           'type': 'album',
                                                           'owner_id': user_id,
                                                           'extended': 1,
                                                           'count': 25,
                                                           'v': '5.131'
                                                           })
        dict_photos = dict()
        try:
            dict_1 = get_photos_id
            list_1 = dict_1['items']
            for i in list_1:
                photo_id = str(i.get('id'))
                i_likes = i.get('likes')
                if i_likes.get('count'):
                    likes = i_likes.get('count')
                    dict_photos[likes] = photo_id
            list_of_ids = sorted(dict_photos.items(), reverse=True)
            return list_of_ids
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photo(self, candidate_information, field):
        if field == 1:
            list = self.get_photos_id(candidate_information)
            count = 0
            for i in list:
                count += 1
                if count == 1:
                    return i[1]
        elif field == 2:
            list = self.get_photos_id(candidate_information)
            count = 0
            for i in list:
                count += 1
                if count == 2:
                    return i[1]
        elif field == 3:
            list = self.get_photos_id(candidate_information)
            count = 0
            for i in list:
                count += 1
                if count == 3:
                    return i[1]


    def send_photo(self, user_id, message, candidate_information, field):
        if field == 1:
            self.vk.method('messages.send', {'user_id': user_id,
                                             'access_token': user_token,
                                             'message': message,
                                             'attachment': f'photo{self.person_id(candidate_information)}_{self.get_photo(self.person_id(candidate_information), 1)}',
                                             'random_id': 0})
        elif field == 2:
            self.vk.method('messages.send', {'user_id': user_id,
                                             'access_token': user_token,
                                             'message': message,
                                             'attachment': f'photo{self.person_id(candidate_information)}_{self.get_photo(self.person_id(candidate_information), 2)}',
                                             'random_id': 0})
        elif field == 3:
            self.vk.method('messages.send', {'user_id': user_id,
                                             'access_token': user_token,
                                             'message': message,
                                             'attachment': f'photo{self.person_id(candidate_information)}_{self.get_photo(self.person_id(candidate_information), 3)}',
                                             'random_id': 0})


    def found_person_info(self, candidate_information):
        return f'{candidate_information[0]} {candidate_information[1]}, ссылка - {candidate_information[3]}, приятного общения!'

    def person_id(self, candidate_information):
        return candidate_information[2]


bot = VK_DateBot()
