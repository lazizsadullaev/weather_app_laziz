import requests
from pprint import pprint
import utils
from db import queries as _db
import config


def get_weather():

    weather_data = []

    username = input('Please enter your username :  ')

    if not _db.check_user_exists('weather.db', username):
        print('[INFO] такого юзера нету')
        _db.add_user('weather.db', username)
        get_weather()
    else:

        while True:
            city = input("Введите название города, в котором хотите узнать погоду: ")

            if city == "show":
                for item in weather_data:
                    print(item)
                else:
                    print('список пустой')

                continue

            if city == "save":

                continue


            config.parameters["q"] = city

            response = requests.get(config.url, params=config.parameters).json()
            # pprint(response)  # dt, temp, name, sunrise, sunset, description, speed

            name = response["name"]
            temp = response["main"]["temp"]
            tz = response["timezone"]
            dt = utils.convert_seconds_to_datetime(seconds=response["dt"], timezone=tz)
            sunrise = utils.convert_seconds_to_datetime(seconds=response["sys"]["sunrise"], timezone=tz)
            sunset = utils.convert_seconds_to_datetime(seconds=response["sys"]["sunset"], timezone=tz)
            description = response["weather"][0]["description"]
            speed = response["wind"]["speed"]

            _db.add_weather('weather.db', weather_id=212,
                        city_name=name,
                        temp=temp,
                        timezone=tz,
                        created_at=dt,
                        sunset=sunset,
                        sunrise=sunrise,
                        description=description,
                        wind_speed=speed,
                        user_id=1)

            weather_data.append(
                utils.make_weather_dict(
                    name=name,
                    temp=temp,
                    tz=tz,
                    dt=dt,
                    sunset=sunset,
                    sunrise=sunrise,
                    description=description,
                    speed=speed
                )
            )

            print(f"""
    ======================================
    В городе {name} сейчас {description}
    Температура воздуха: {temp} •C
    Скорость ветра: {speed} м/c
    Время отправки запроса: {dt}
    Время восхода солнца: {sunrise}
    Время заката солнца: {sunset}
    ======================================
    """)
