import requests


def squadron_search(name: str, count: int = 1) -> dict:
    """Поиск полка по названию."""
    url = f'https://api.thunderinsights.dk/v1/clans/direct/clan/search/?clan={name}&limit={count}'

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


def user_search(username: str, count: int = 2) -> dict:
    """Поиск пользователя по никнейму."""
    url = f'https://api.thunderinsights.dk/v1/users/direct/search/?nick={username}&limit={count}'

    response = requests.get(url)

    response = response.json()

    try:
        response['userid']
    except TypeError:
        response = response[0]

    context = {
        'name': response['nick'],
        'id': response['userid'],
        'clan_tag': response['clan_tag'],
        'clan_name': response['clan_name']
    }

    return context


def get_user(user_id: int) -> dict:
    """Поиск пользователя по user_id."""
    url = f'https://api.thunderinsights.dk/v1/users/direct/terse/?userid={user_id}'

    response = requests.get(url)

    response = response.json()

    response = response[str(user_id)]

    context = {
        'name': response['nick'],
        'id': str(user_id),
        'clan_Tag': response['clanTag'],
        'clan_name': response['clanName']
    }

    return context
