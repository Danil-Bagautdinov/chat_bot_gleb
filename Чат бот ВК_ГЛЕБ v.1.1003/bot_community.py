import bs4 as bs4
import pyowm
import pymorphy2
import requests
from bs4 import BeautifulSoup
from translate import Translator
morph = pymorphy2.MorphAnalyzer()


class VkBot:

    def __init__(self, user_id):
        print("\nСоздан бот!")

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "КАК ДЕЛА?", "ПОКА", "ТЫ ДУРАК", "ЗДРАСТЕ",
                          "ВЫПЬЕМ", "ПРИВЕТ АЛИСА",
                          "АРТУР САДЫКОВ", "САДЫКОВ АРТУР", "БАГАУТДИНОВ ДАНИЛ", "ДАНИЛ БАГАУТДИНОВ",
                          'ПОГОДЫ', 'ПОМОЩЬ', 'ПЕРЕВЕДИ', 'СКАЖИ КУРС', 'КУРС ВАЛЮТ', 'КУРС',
                          "КАКОЙ КУРС ВАЛЮТ", "СКАЖИ КУРС ВАЛЮТ", "КОРОНАВИРУС", "COVID-19"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}!"

        # Помощь
        elif message.upper() == 'НАЧАТЬ' or message.upper() == 'ПОМОЩЬ':
            return 'Приветствую! 👋' '\n' 'Меня зовут Глеб. Я чат бот. 🤖' '\n' \
                   'Мои команды: "Привет",' \
                    ' "Как дела?", "Ты дурак", "Выпьем", "Данил Багаутдинов", "Артур Садыков",' \
                    ' "Багаутдинов Данил", "Садыков Артур", "Погода в (ваш город)",' \
                    ' "Прогноз погоды в (ваш город)", "Время", "Привет Алиса", "Пока", "Здрасте",' \
                   ' "Помощь", "Переведи (текст)", "COVID-19", "Коронавирус"'

        # Погода
        elif self._COMMANDS[1] in message.upper() or self._COMMANDS[13] in message.upper():
            try:
                # Если пользователь хочет узнать долгосрочный прогноз - идём сюда..
                if 'ПРОГНОЗ' in message.upper():
                    # Вытаскиваем из комманды название города
                    city_name = message.split()
                    # Склоняем название в именительный падеж
                    return self._get_weather_3h(morph.parse(city_name[3])[0].inflect(
                        {'sing', 'nomn'}).word.title())
                # ...иначе сюда..
                else:
                    # Вытаскиваем из комманды название города
                    city_name = message.split()
                    # Склоняем название в именительный падеж
                    return self._get_weather(morph.parse(city_name[2])[0].inflect(
                        {'sing', 'nomn'}).word.title())
            except:
                return 'Ой, что-то не так, повтори ещё разок.' '\n' \
                       'Внимание: команда должна иметь вид,' \
                       'к примеру: Погода в Азнакаево или Прогноз погоды в Азнакаево' '\n' '' \
                       'Необязательно с заглавной буквы, можно писать по разному, главное, ' \
                       'что это должен быть существующий город в России.'

        # Время
        elif message.upper() == self._COMMANDS[2]:
            return self._get_time()

        # Как дела?
        elif message.upper() == self._COMMANDS[3]:
            return f"Все норм, {self._USERNAME}! ☺"

        # Пока
        elif message.upper() == self._COMMANDS[4]:
            return f"Пока, {self._USERNAME}! 😉"

        # Общение
        elif message.upper() == self._COMMANDS[5]:
            return f"Кто обзывается, тот сам так называется! 😛"

        elif message.upper() == self._COMMANDS[6]:
            return f"Здарова, {self._USERNAME}! 🖐🏻"

        elif message.upper() == self._COMMANDS[7]:
            return "Я не пью!"

        elif message.upper() == self._COMMANDS[8]:
            return "Я ГЛЕБ! 😑"

        elif message.upper() == self._COMMANDS[9]:
            return f"Ох, {self._USERNAME}, я с ним очен хорошо знаком. Он мой создатель!"

        elif message.upper() == self._COMMANDS[10]:
            return f"Ох, {self._USERNAME}, я с ним очен хорошо знаком. Он мой создатель!"

        elif message.upper() == self._COMMANDS[11]:
            return f"Оляля, {self._USERNAME}, вы с ним знакомы? Он мой создатель! " \
                f"[id174238358|Создатель]"

        elif message.upper() == self._COMMANDS[12]:
            return f"Оляля, {self._USERNAME}, вы с ним знакомы? Он мой создатель!"

        # Переводчик
        elif self._COMMANDS[15] in message.upper():
            return self._get_translation(message)

        # Курс валют
        elif message.upper() == self._COMMANDS[16]:
            return self._get_exchange_rates()

        elif message.upper() == self._COMMANDS[17]:
            return self._get_exchange_rates()

        elif message.upper() == self._COMMANDS[18]:
            return self._get_exchange_rates()

        elif message.upper() == self._COMMANDS[19]:
            return self._get_exchange_rates()

        elif message.upper() == self._COMMANDS[20]:
            return self._get_exchange_rates()

        elif message.upper() == self._COMMANDS[21]:
            return self._get_covid19_cases()

        elif message.upper() == self._COMMANDS[22]:
            return self._get_covid19_cases()

        else:
            return "Не понимаю о чем вы. 🤨"

    # Время
    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    # Функция для очистки от ненужных тэгов
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

    # Долгосрочный прогноз
    @staticmethod
    def _get_weather_3h(city_name):
        try:
            owm = pyowm.OWM('cd663094c13260b015bc50ecf134be54')
            count = 0
            fc = owm.three_hours_forecast(f'{city_name},ru')
            f = fc.get_forecast()
            list = []
            for weather in f:
                g = weather.get_reference_time('iso'), weather.get_status()
                count += 1
                # в "f" содержится 40 данных о погоде на протяжении 5 дней каждые 3 часа
                # поэтому берем только часть, а именно прогноз на три дня
                if count != 24:
                    list.append(g)
                else:
                    list.append('Формат времени указан в UTC')
                    return '\n'.join(map(str, list))
        except:
            return 'Что-то сломалось, но, главное, что мы не упали...'

    # Погода
    @staticmethod
    def _get_weather(city_name):
        try:
            # API - ключ сайта с прогнозами погоды
            owm = pyowm.OWM('cd663094c13260b015bc50ecf134be54')

            # Получение информации о погоде
            observation = owm.weather_at_place(f'{city_name},RU')
            weather = observation.get_weather()

            # Получени статуса погода, например: Облачно
            weather_stat = weather.get_status()

            # Получение значения давления
            pressure = weather.get_pressure()['press']

            # Получение значения скорости ветра
            wind_speed = weather.get_wind()['speed']

            # Получение значения направления ветра в градусах
            wind_direction = weather.get_wind()['deg']

            # Получение значения влажности воздуха
            humidity = weather.get_humidity()

            # Получение времени восхода Солнца
            sunrise_time = weather.get_sunrise_time('iso')

            # Получение времени заката Солнца
            sunset_time = weather.get_sunset_time('iso')

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
            temperature_max = weather.get_temperature('celsius')['temp_max']
            temperature_min = weather.get_temperature('celsius')['temp_min']
            if weather_stat == 'Clouds':
                weather_status = 'Облачно ☁'
            elif weather_stat == 'Rain':
                weather_status = 'Дождь 🌧'
            elif weather_stat == 'Snow':
                weather_status = 'Снег 🌨'
            else:
                weather_status = 'Солнечно ☀'

            # И, наконец, сбор всех данных воедино
            return ('Дай-ка подумать 🔮' '\n' f'Температура 🌡: Сейчас в городе {city_name} '
                    f'{temperature}℃.'
                    '\n' f'Max сут. температура: {temperature_max}℃' 
                    '\n' f'Min сут. температура: {temperature_min}℃'
                    '\n' f'Статус: {weather_status}' '\n' f'Давление: {pressure} мм.рт.ст.' '\n'
                    f'Ветер 💨: {wind_direction_word}, {wind_speed} м/с' 
                    '\n' f'Влажность воздуха 💦: {humidity}%'
                    '\n' f'Восход 🌅: {sunrise_time}' '\n' f'Закат 🌇: {sunset_time}'
                    '\n' '*время по UTC')
        except:
            return 'Ой, что-то не так, повтори ещё разок (Внимание: город должен быть в России!)'

    # Функция переводчика
    @staticmethod
    def _get_translation(message):
        translator = Translator(to_lang='Russian')
        text = message.split()
        new_text = ' '.join(map(str, text[1:]))
        return translator.translate(' '.join(map(str, text[1:])))

    # Функция курса валют
    @staticmethod
    def _get_exchange_rates():
        url = 'https://www.cbr.ru/currency_base/daily/'

        source = requests.get(url)
        main_text = source.text
        soup = BeautifulSoup(main_text)

        table = soup.find('div', {'class': 'table-wrapper'})
        table = table.findAll('td', {'class': ''})
        return('Свежайший курс валют из сайта ЦБ России 💹' '\n' 
               f'{table[53].text} 🇺🇸: {table[54].text[:-2]}₽ за один $' '\n' f'{table[58].text} 🇪🇺: '
               f'{table[59].text[:-2]}₽ за один €')

    # Статистика заражения COVID-19 в России
    @staticmethod
    def _get_covid19_cases():
        url = 'https://www.worldometers.info/coronavirus/country/russia/'

        source = requests.get(url)
        main_text = source.text
        soup = BeautifulSoup(main_text)

        tab = soup.findAll('div', {'class': 'maincounter-number'})
        return ('Статистика заражения COVID-19 в России' '\n' 
                f'Подтверждено 😷: {tab[0].text}'
                f'Выздоровело 🏥: {tab[2].text}' 
                f'Летальные исходы 💀: {tab[1].text}')
