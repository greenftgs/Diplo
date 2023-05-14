import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError, AuthError, ApiHttpError
from config import vk_token

vk_app = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(vk_app)


def msg_bot():
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text
                return message_text, this_event.user_id


def send_message(user_id, message, attachment=None):
    params = {
        'user_id': user_id,
        'message': message,
        'attachment': attachment,
        'random_id': get_random_id()
    }
    try:
        vk_app.method('messages.send', params)
    except (AuthError, ApiError, ApiHttpError) as err:
        print(f'Ошибка {str(err)}, попробуйте снова')


if __name__ == '__main__':
    pass
