from datetime import datetime
from random import randint
import time
import requests
import vk_api
from vk_api.exceptions import ApiError, AuthError, ApiHttpError
from config import *
from message import send_message, msg_bot

token = vk_api.VkApi(token=user_token)
gr_token = vk_api.VkApi(token=vk_token)


class VkTools:
    def __init__(self):
        self.token = vk_api.VkApi(token=user_token)
        self.gr_token = vk_api.VkApi(token=vk_token)

    def get_info(user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_id': user_id,
                  'fields': 'first_name, last_name, bdate, sex, city',
                  'v': 5.131}

        res = requests.get(url, params=params)
        response_json = res.json()

        try:
            sex = response_json['response'][0]['sex']
            if sex != 0:
                sex = 3 - sex

            else:
                send_message(user_id, 'Пожалуйста укажите свой пол. Введите: \n'
                                      '1 - девушка\n2 - парень')
                message_text, user_id = msg_bot()
                sex = message_text[:]
                if sex == 1:
                    sex = 2
                elif sex == 2:
                    sex = 1
                else:
                    send_message(user_id, 'Нет такого значения!')

            if 'bdate' in response_json['response'][0].keys() and \
                    len(response_json['response'][0]['bdate'].split('.')) == 3:
                birth_year = int(response_json['response'][0]['bdate'][-4:])
                from_age = (int(datetime.now().year) - birth_year) - 5
                to_age = (int(datetime.now().year) - birth_year) + 5

            else:
                send_message(user_id, 'Введите минимальный возраст\n'
                                      ' для поиска (две цифры, например: 21): ')
                message_text, user_id = msg_bot()
                from_age = message_text[0:1]
                send_message(user_id, 'Введите максимальный возраст для\n'
                                      ' поиска (две цифры, например: 55): ')
                message_text, user_id = msg_bot()
                to_age = message_text[0:1]

            if 'city' in response_json['response'][0]:
                city_id = response_json['response'][0]['city']['id']

            else:
                send_message(user_id, 'Введите город для поиска')
                message_text, user_id = msg_bot()
                city = message_text[0:len(message_text)].lower()
                city_id = 0
                response = token.method("database.getCities",
                                        {"country_id": 1,
                                         "q": f'{city}',
                                         "need_all": 0,
                                         "count": 100})
                if response['count']:
                    city_id = response['items'][0]['id']

            return user_id, sex, from_age, to_age, city_id

        except (AuthError, ApiError, ApiHttpError) as err:
            send_message(user_id, f'Возникла ошибка {str(err)}, попробуйте обновить токен либо нет доступа к фото')

    def upload_photo(owner_id):
        try:
            response = token.method('photos.get', {
                'access_token': user_token,
                'owner_id': owner_id,
                'album_id': 'profile',
                'extended': 1,
                'v': '5.131'})

            user_photo = []
            for photo in response['items']:
                if response['items'] is None:
                    continue
                else:
                    url = photo['sizes'][-1]['url']
                    count_likes_and_comments = photo['likes']['count'] + photo['comments']['count']
                    user_photo.append((count_likes_and_comments, url))

            user_photo.sort(reverse=True)

            best_photo = []
            for photo in user_photo[:3]:
                best_photo.append(photo)

            return best_photo

        except (AuthError, ApiError, ApiHttpError) as err:
            send_message(owner_id, f'Возникла ошибка {str(err)}, нет доступа к фото')

    def search_people(sex, from_age, to_age, city_id):
        try:
            response = token.method('users.search', {
                'sex': sex,
                'city_id': city_id,
                'age_from': from_age,
                'age_to': to_age,
                'has_photo': 1,
                'status': '1' or '6' or '0',
                'is_closed': 1,
                'offset': randint(0, 100),
                'count': 1,
                'v': '5.131'})

            time.sleep(0.5)

            result_list_dict = {}
            for item in response['items']:
                first_name = item.get("first_name")
                last_name = item.get("last_name")
                owner_id = item.get("id")
                url_owner = 'https://vk.com/id' + str(owner_id)
                photos = VkTools.upload_photo(owner_id)
                key, value = f'{owner_id}', [first_name, last_name, url_owner, photos]
                result_list_dict.update({key: value})
            return result_list_dict
        except (AuthError, ApiError, ApiHttpError) as err:
            print(f'Возникла ошибка {str(err)}, попробуйте обновить токен')


if __name__ == '__main__':
    pass
    # user_id =
    # user_info = VkTools.get_info(user_id)
    # match = VkTools.search_people(sex=user_info[1], from_age=user_info[2], to_age=user_info[3],
    #                            city_id=user_info[4])
    # print(match)
