import requests
import vk_api
from io import BytesIO
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randrange
from vk.search import get_potential_friends, get_potential_friend_photos, VkClient
from db.db_control import Vkinder
from environs import Env

env = Env()
env.read_env()
vk_auth = vk_api.VkApi(token=env('API_GROUP_TOKEN'))
vk = vk_auth.get_api()
longpoll = VkLongPoll(vk_auth)
upload = VkUpload(vk_auth)
vk_client = VkClient(env('VK_TOKEN'))
vkinder = Vkinder()

users_requests = {"city": "", "sex": "", "age": ""}


def send_message(user_id, message, keyboard=None):
    text = {"user_id": user_id, "message": message, "random_id": randrange(10**7)}
    if keyboard is not None:
        text["keyboard"] = keyboard.get_keyboard()
    vk_auth.method("messages.send", text)


def start(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Начнём подбор!", VkKeyboardColor.PRIMARY)
    send_message(user_id, "Привет", keyboard)


def finish(user_id):
    send_message(user_id, "Всего доброго! До скорых встреч!")


def get_city(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Завершить", color=VkKeyboardColor.NEGATIVE)
    send_message(user_id, "В каком городе будем искать?", keyboard)


def confirm_city(user_id, city):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Да, город верный", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Изменить город", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Завершить", color=VkKeyboardColor.NEGATIVE)
    send_message(user_id, f"Ищем в городе {city.capitalize()}?", keyboard)


def get_sex(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Парня", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Девушку", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Завершить", color=VkKeyboardColor.NEGATIVE)
    send_message(user_id, "Кого будем искать?", keyboard)


def get_age(user_id):
    send_message(user_id, "Укажите возраст:")


def confirm_all_data(user_id, sex, city, age):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Все верно", VkKeyboardColor.SECONDARY)
    keyboard.add_button("Изменить параметры", VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_message(
        user_id,
        f"Ищем {sex} в возрасте {age} из города {city.capitalize()}?",
        keyboard,
    )


def change_all_data(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Город", VkKeyboardColor.PRIMARY)
    keyboard.add_button("Пол", VkKeyboardColor.POSITIVE)
    keyboard.add_button("Возраст", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_message(user_id, "Что хотите изменить?", keyboard)


def send_match(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Давай смотреть!", VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_message(
        user_id,
        f"По вашему запросу найдено {len(vkinder.search_user(user_id))} пользователей!",
        keyboard,
    )


def send_photo(user_id, url):
    vk.messages.send(user_id=user_id, attachment=url, random_id=randrange(10**7))


def send_next(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("В чёрный список", VkKeyboardColor.NEGATIVE)
    keyboard.add_button("Дальше", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("ИЗБРАННОЕ", VkKeyboardColor.PRIMARY)
    keyboard.add_button("В избранное", VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_message(user_id, "Что думаете о данном пользователе?", keyboard)


def send_next_v2(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Дальше", VkKeyboardColor.POSITIVE)
    keyboard.add_button("Избранное", VkKeyboardColor.PRIMARY)
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_message(user_id, "Смотрим дальше?", keyboard)


def add_to_blacklist(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Избранное", VkKeyboardColor.PRIMARY)
    keyboard.add_button("Дальше", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_message(user_id, "Пользователь добавлен в чёрный список", keyboard)


def friends_list():
    friends = get_potential_friends(
        client=vk_client,
        sex=users_requests["sex"],
        city=users_requests["city"],
        age=users_requests["age"],
    )
    return friends


def main():
    flag = ""
    count = 0
    new_city = ""
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.message.lower()
            client_id = event.user_id
            if msg and flag == "":
                start(client_id)
                flag = "start"
            if msg == "завершить":
                finish(client_id)
                flag = ""
            elif msg == "начнём подбор!":
                vkinder.drop_tables()
                vkinder.create_tables()
                get_city(client_id)
                flag = "to_city"
            elif flag == "to_city":
                confirm_city(client_id, msg)
                flag = msg
            elif msg == "да, город верный" and flag != "confirm data":
                city = flag
                users_requests["city"] = city.capitalize()
                flag = "to_sex"
                get_sex(client_id)
            elif msg == "изменить город":
                get_city(client_id)
                if users_requests["sex"] == "":
                    flag = "to_city"
                else:
                    flag = "change city"
            elif msg == "парня" and flag != "change sex":
                sex = msg
                users_requests["sex"] = "1"
                get_age(client_id)
                flag = "to_age"
            elif msg == "девушку" and flag != "change sex":
                sex = msg
                users_requests["sex"] = "2"
                get_age(client_id)
                flag = "to_age"
            elif flag == "to_age":
                try:
                    age = msg.strip()
                    users_requests["age"] = age
                    flag = "confirm"
                    confirm_all_data(
                        user_id=client_id,
                        sex=sex,
                        city=users_requests["city"],
                        age=users_requests["age"],
                    )
                except ValueError:
                    send_message(client_id, "Что-то пошло не так")
                    get_age(client_id)
            elif msg == "изменить параметры":
                change_all_data(client_id)
            elif msg == "город":
                get_city(client_id)
                flag = "change city"
            elif flag == "change city":
                flag = "confirm data"
                new_city = msg
                confirm_city(client_id, msg)
            elif msg == "да, город верный" and flag == "confirm data":
                city = new_city
                users_requests["city"] = city.capitalize()
                confirm_all_data(
                    user_id=client_id,
                    city=users_requests["city"],
                    sex=users_requests["sex"],
                    age=users_requests["age"],
                )
            elif msg == "возраст":
                get_age(client_id)
                flag = "to_age"
            elif msg == "пол":
                flag = "change sex"
                get_sex(client_id)
            elif msg == "парня" and flag == "change sex":
                sex = msg
                users_requests["sex"] = "1"
                confirm_all_data(
                    user_id=client_id,
                    sex=sex,
                    city=users_requests["city"],
                    age=users_requests["age"],
                )
            elif msg == "девушку" and flag == "change sex":
                sex = msg
                users_requests["sex"] = "2"
                confirm_all_data(
                    user_id=client_id,
                    sex=sex,
                    city=users_requests["city"],
                    age=users_requests["age"],
                )
            elif msg == "все верно":
                vkinder.add_user_data(friends_list())
                send_match(client_id)
                count = 0
            elif msg == "давай смотреть!" or msg == "дальше":
                count += 1
                user = vkinder.get_one_user(user_id=count)
                full_name = f"{user.name} {user.surname}"
                page_link = f"https://vk.com/id{user.user_id}"
                photo_list = get_potential_friend_photos(
                    vk_client, owner_id=user.user_id
                )
                blocked = vkinder.check_blacklist(user.user_id)
                favourited = vkinder.check_favorites(user.user_id)
                if blocked:
                    send_message(client_id, full_name)
                    send_message(client_id, page_link)
                    send_message(
                        client_id,
                        "Пользователь добавлен в чёрный список, поэтому Вам не будут показаны его фото.",
                    )
                    send_next_v2(client_id)
                else:
                    if favourited:
                        send_message(client_id, full_name)
                        send_message(client_id, page_link)
                        send_message(
                        client_id,
                            "Пользователь уже добавлен в избранное.",
                        )
                        send_next_v2(client_id)
                    else:
                        if photo_list is not None:
                            vkinder.add_photo_urls(user.user_id, photo_list)
                            send_message(client_id, full_name)
                            send_message(client_id, page_link)
                            user_photos = vkinder.get_photo_urls(user.user_id)
                            for photo in user_photos:
                                img = requests.get(photo.url).content
                                f = BytesIO(img)
                                upload_photo = upload.photo_messages(f)[0]
                                url = "photo{}_{}".format(
                                    upload_photo["owner_id"], upload_photo["id"]
                                )
                                send_photo(client_id, url=url)
                            send_next(client_id)
                        else:
                            send_message(client_id, full_name)
                            send_message(client_id, page_link)
                            send_message(
                                client_id,
                                "У пользователя недостаточно фото, можете перейти по ссылке на его страницу!",
                            )
                            send_next(client_id)
            elif msg == "в избранное":
                vkinder.add_to_favorites(user.user_id)
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("ИЗБРАННОЕ", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Дальше", VkKeyboardColor.SECONDARY)
                keyboard.add_line()
                keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
                send_message(
                    client_id,
                    f"Пользователь добавлен в избранное!",
                    keyboard,
                )
            elif msg == "избранное":
                favorites = vkinder.get_all_from_favorites()
                send_message(client_id, f"У Вас в избранном {len(favorites)} человек:")
                for favorite in favorites:
                    user = vkinder.search_user(user_id=favorite.user_id)
                    full_name = f"{user.name} {user.surname}"
                    page_link = f"https://vk.com/id{user.user_id}"
                    send_message(client_id, f"{full_name} {page_link}")
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Дальше", VkKeyboardColor.SECONDARY)
                keyboard.add_line()
                keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
                send_message(client_id, "Смотрим дальше?", keyboard)
            elif msg == "в чёрный список":
                vkinder.add_to_blacklist(user.user_id)
                add_to_blacklist(client_id)


if __name__ == "__main__":
    main()
