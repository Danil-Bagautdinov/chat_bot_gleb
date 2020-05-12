import bs4 as bs4
import requests
import pyowm
import pymorphy2


morph = pymorphy2.MorphAnalyzer()


class VkBot:

    def __init__(self, user_id):
        print("\nСоздан бот!")

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "КАК ДЕЛА?", "ПОКА", "ТЫ ДУРАК", "ЗДРАСТЕ",
                          "ВЫПЬЕМ", "ПРИВЕТ АЛИСА",
                          "АРТУР САДЫКОВ", "САДЫКОВ АРТУР", "БАГАУТДИНОВ ДАНИЛ", "ДАНИЛ БАГАУТДИНОВ"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}!"
        # Погода
        elif self._COMMANDS[1] in message.upper():
                # Вытаскиваем из комманды название города
                city_name = message.split()
                # Склоняем название в именительный падеж
                return self._get_weather(morph.parse(city_name[2])[0].inflect(
                    {'sing', 'nomn'}).word.title())
        # Время
        elif message.upper() == self._COMMANDS[2]:
            return self._get_time()
        # Как дела?
        elif message.upper() == self._COMMANDS[3]:
            return f"Все норм, {self._USERNAME}!"

        # Пока
        elif message.upper() == self._COMMANDS[4]:
            return f"Пока, {self._USERNAME}!"

        # Общение
        elif message.upper() == self._COMMANDS[5]:
            return f"Кто обзывается, тот сам так называется!"

        elif message.upper() == self._COMMANDS[6]:
            return f"Здарова, {self._USERNAME}!"

        elif message.upper() == self._COMMANDS[7]:
            return "Я не пью!"

        elif message.upper() == self._COMMANDS[8]:
            return "Я ГЛЕБ!"

        elif message.upper() == self._COMMANDS[9]:
            return f"Ох, {self._USERNAME}, я с ним очен хорошо знаком. Он мой создатель!"

        elif message.upper() == self._COMMANDS[10]:
            return f"Ох, {self._USERNAME}, я с ним очен хорошо знаком. Он мой создатель!"

        elif message.upper() == self._COMMANDS[11]:
            return f"Оляля, {self._USERNAME}, вы с ним знакомы? Он мой создатель!"

        elif message.upper() == self._COMMANDS[12]:
            return f"Оляля, {self._USERNAME}, вы с ним знакомы? Он мой создатель!"
        else:
            return "Не понимаю о чем вы"

    # Время
    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    @staticmethod
    def _clean_all_tag_from_str(string_line):
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        return result

    # Погода
    @staticmethod
    def _get_weather(city_name):

        # API - ключ сайта с прогнозами погоды
        owm = pyowm.OWM('cd663094c13260b015bc50ecf134be54')

        # Получение информации о погоде
        observation = owm.weather_at_place(f'{city_name},RU')
        weather = observation.get_weather()
        weather_stat = weather.get_status()
        pressure = weather.get_pressure()['press']
        wind_speed = weather.get_wind()['speed']
        wind_direction = weather.get_wind()['deg']

        # Направление ветра из градусов в стороны света
        if wind_direction == 0 or wind_direction == 360:
            wind_direction_word = 'С'
        elif wind_direction in range(1, 90):
            wind_direction_word = 'С-В'
        elif wind_direction == 90:
            wind_direction_word = 'В'
        elif wind_direction in range(91, 180):
            wind_direction_word = 'Ю-В'
        elif wind_direction == 180:
            wind_direction_word = 'Ю'
        elif wind_direction in range(181, 270):
            wind_direction_word = 'Ю-З'
        elif wind_direction == 270:
            wind_direction_word = 'З'
        elif wind_direction in range(271, 360):
            wind_direction_word = 'С-З'

        # Предписание статуса погоды
        temperature = weather.get_temperature('celsius')['temp']
        if weather_stat == 'Clouds':
            weather_status = 'Облачно ☁'
        elif weather_stat == 'Rain':
            weather_status = 'Дождь 🌧'
        elif weather_stat == 'Snow':
            weather_status = 'Снег 🌨'
        else:
            weather_status = 'Солнечно ☀'

        # И, наконец, сбор всех данных воедино
        return ('Дай-ка подумать 🔮' '\n' f'Температура в городе {city_name} {temperature}℃.'
                '\n' f'Статус: {weather_status}' '\n' f'Давление 🌡: {pressure} мм.рт.ст.' '\n'
                f'Ветер 💨: {wind_direction_word}, {wind_speed} м/с')
