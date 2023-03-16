from django.db.models import Q, QuerySet

from geo.clients.shemas import WeatherInfoDTO
from geo.clients.weather import WeatherClient
from geo.models import Weather


class WeatherService:
    """
    Сервис для работы с данными о погоде.
    """

    def get_weather(self, alpha2code: str, city: str) -> QuerySet[Weather]:
        """
        Получение погоды в выбранном городе.

        :param alpha2code: ISO Alpha2 код страны
        :param city: Город
        :return:
        """

        weather = Weather.objects.filter(Q(country__iregex=alpha2code) | Q(city__iregex=city))

        if not weather:
            if data := WeatherClient().get_weather(f"{city},{alpha2code}"):
                self.build_model(data)
                weather = Weather.objects.filter(Q(country__iregex=alpha2code) | Q(city__iregex=city))

        return weather

    @staticmethod
    def build_model(weather: WeatherInfoDTO) -> Weather:
        """
        Формирование объекта модели погоды.

        :param WeatherInfoDTO weather: Данные о погоде.
        :return:
        """

        return Weather.objects.create(
            country=weather.country,
            city=weather.city,
            temp=weather.temp,
            pressure=weather.pressure,
            humidity=weather.humidity,
            wind_speed=weather.wind_speed,
            description=weather.description,
        )
