from django.core.cache import cache
import requests


def getDataCrypto():
    cache_key = 'global_var'
    dataCrypto = cache.get(cache_key)
    if dataCrypto is None:
        response = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=99999999&page=1&sparkline=false"
            )
        dataCrypto = response.json()
        cache.set(cache_key, dataCrypto, timeout=60*60)  # almacenar en caché durante 1 hora
    return dataCrypto