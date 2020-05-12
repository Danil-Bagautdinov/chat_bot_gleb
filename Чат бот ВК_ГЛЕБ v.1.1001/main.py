import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from commander.commander import Commander
from vk_bot import VkBot


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,
                                'random_id': random.randint(0, 2048)})


# API-ключ
token = "98d5cef082fe5624912e27fd0a41fb131b1300b64d68f23552fc8b1205f4e58ff27ee3d0049ccefaa55fd"

# Авторизуемся
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

commander = Commander()
print("Server started")
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            print(f'New message from {event.user_id}', end='')

            bot = VkBot(event.user_id)

            if event.text[0] == "/":
                write_msg(event.user_id, commander.do(event.text[1::]))
            else:
                write_msg(event.user_id, bot.new_message(event.text))

            print('Text: ', event.text)
            print("============================")
