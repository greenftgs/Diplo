from vk_func import *
from database import *
from vk_api.longpoll import VkEventType
from message import longpoll


class App(VkTools):

    @staticmethod
    def bot_listen():
        create_tables(engine)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text.lower()
                if request in ['1', 'привет', 'прив', 'привт', 'ghbdtn']:
                    send_message(event.user_id, f'Добро пожаловать.\n'
                                                f'Давай найдём тебе пару! Напиши "2" или "Найти"')

                elif request in ['найти', '2', 'ещё', 'ЕЩЁ', '3']:
                    user_info = VkTools.get_info(event.user_id)
                    found_users_list = VkTools.search_people(sex=user_info[1], from_age=user_info[2],
                                                             to_age=user_info[3], city_id=user_info[4])

                    list_without_viewed = {}
                    found_users_list.items()
                    if sorted_users_by_viewed(tuple(found_users_list.keys())) is True:
                        for key, value in found_users_list.items():
                            list_without_viewed[key] = value
                            if len(list_without_viewed) == 0:
                                continue

                    else:
                        found_users_list = VkTools.search_people(sex=user_info[1], from_age=user_info[2],
                                                                 to_age=user_info[3], city_id=user_info[4])
                        if sorted_users_by_viewed(tuple(found_users_list.keys())) is True:
                            for key, value in found_users_list.items():
                                list_without_viewed[key] = value
                                if len(list_without_viewed) == 0:
                                    continue

                    dict_to_sent = {}
                    for value in list_without_viewed.values():
                        dict_to_sent = ' '.join(str(x) for x in value)
                        if len(dict_to_sent) == 0:
                            continue

                    send_message(event.user_id, str(dict_to_sent))
                    for i in found_users_list.keys():
                        add_user(i)
                    send_message(event.user_id, f'Напиши "ЕЩЁ" или "3" для повторного поиска\n'
                                                f' либо "Выход", чтобы остановить бот')

                elif request in ['выход', 'Выход']:
                    send_message(event.user_id, f'Надёюсь ты нашёл, кого-то, а если нет, то заходи ещё!')
                    break


if __name__ == '__main__':
    App.bot_listen()
