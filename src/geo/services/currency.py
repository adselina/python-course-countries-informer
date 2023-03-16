
from django.db.models import Q, QuerySet

from geo.clients.currency import CurrencyClient
from geo.models import CurrencyRate


class CurrencyService:
    """
    Сервис для работы с данными о курсах валют.
    """

    def get_currency(self, base: str = "rub") -> QuerySet[CurrencyRate]:
        """
        Получение курсов валют по отношению к базовой валюте.
        :param base: Название валюты
        :return:
        """

        currency_rates = CurrencyRate.objects.filter(Q(base__iregex=base))

        if not currency_rates:
            if data := CurrencyClient().get_currency(base):
                for key, value in data.rates.items():
                    self.build_model(data.base, data.date, key, value)
                currency_rates = CurrencyRate.objects.filter(Q(base__iregex=base))

        return currency_rates

    @staticmethod
    def build_model(base: str, date: str, compared: str, value: float) -> CurrencyRate:
        """
        Создание модели валюты
        :param base: Валюта.
        :param date: Дата получения курса.
        :param compared: Валюта для сравнения.
        :param value: Курс валют.
        :return:
        """

        return CurrencyRate.objects.create(
            base=base,
            date=date,
            compared_to=compared,
            value=value,
        )
