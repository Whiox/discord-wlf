import requests


def squadron_search(name: str, count: int = 1) -> dict:
    """Поиск полка по названию"""
    url = f'https://api.thunderinsights.dk/v1/clans/direct/clan/search/?clan={name}&limit=1'

    response = requests.get(url)

    response = response.json()

    try:
        response['clan']['name']
    except TypeError:
        response['clan'] = response['clan'][0]

    context = {
        'name': response['clan']['name'],
        'id': response['clan']['_id'],
        'status': response['clan']['status'],
        'tag': response['clan']['lastPaidTag'],
        'slogan': response['clan']['slogan'],
        'member_count': response['clan']['members_cnt']
    }

    return context
