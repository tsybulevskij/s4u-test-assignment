import requests


class Exchange(object):
    api_url = 'http://api.fixer.io/latest'

    @staticmethod
    def get_rate(from_currency, to_currency):
        if from_currency == to_currency:
            return 1
        result = requests.get(Exchange.api_url, params={
            'base': from_currency,
            'symbols': to_currency
        })
        if result.status_code == 200:
            return result.json()['rates'][to_currency]
        else:
            raise Exception('Eror during get exchange rate')