from pprint import pprint

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
    """Поиск пользователя по username."""
    url = f'https://api.thunderinsights.dk/v1/users/direct/search/?nick={username}&limit={count}'

    response = requests.get(url)

    response = response.json()

    try:
        response['userid']
    except TypeError:
        response = response[0]
    except KeyError:
        return {'id': 0}

    context = {
        'name': response.get('nick', 0),
        'id': response.get('userid', 0),
        'clan_Tag': response.get('clanTag', 0),
        'clan_name': response.get('clanName', 0)
    }

    return context


def get_user(user_id: int) -> dict:
    """Поиск пользователя по user_id."""
    url = f'https://api.thunderinsights.dk/v1/users/direct/terse/?userid={user_id}'

    response = requests.get(url)

    response = response.json()

    response = response[str(user_id)]

    context = {
        'name': response.get('nick', 0),
        'id': response.get('_id', 0),
        'clan_Tag': response.get('clanTag', 0),
        'clan_name': response.get('clanName', 0)
    }

    return context


def get_user_data(user_id: int) -> dict:
    """Получить информацию о пользователе по user_id."""
    url = f'https://api.thunderinsights.dk/v1/users/direct/{user_id}'
    response = requests.get(url).json()

    def extract_air_stats(data: dict) -> dict:
        return {
            'kills_total': data.get('kills_player_or_bot', {}).get('value_total', 0),
            'kills_player': data.get('air_kills_player', {}).get('value_total', 0),
            'total_sessions': data.get('each_player_session', {}).get('value_total', 0),
            'victories_sessions': data.get('each_player_victories', {}).get('value_total', 0),
            'total_deaths': data.get('air_death', {}).get('value_total', 0),
            'air_deaths': data.get('air_death', {}).get('value_total', 0),
            'average_score': data.get('averageScore', {}).get('value_total', 0),
            'total_spawns': data.get('air_spawn', {}).get('value_total', 0),
            'relative_position': data.get('averageRelativePosition', {}).get('value_total', 0),
        }

    def extract_tank_stats(data: dict) -> dict:
        return {
            'kills_total': data.get('kills_player_or_bot', {}).get('value_total', 0),
            'kills_player': data.get('ground_kills_player', {}).get('value_total', 0) + data.get('air_kills_player', {}).get('value_total', 0),
            'total_sessions': data.get('each_player_session', {}).get('value_total', 0),
            'victories_sessions': data.get('each_player_victories', {}).get('value_total', 0),
            'total_deaths': data.get('ground_death', {}).get('value_total', 0) + data.get('air_death', {}).get('value_total', 0),
            'air_deaths': data.get('air_death', {}).get('value_total', 0),
            'ground_deaths': data.get('ground_death', {}).get('value_total', 0),
            'average_score': data.get('averageScore', {}).get('value_total', 0),
            'total_spawns': data.get('ground_spawn', {}).get('value_total', 0) + data.get('air_spawn', {}).get('value_total', 0),
            'relative_position': data.get('averageRelativePosition', {}).get('value_total', 0),
        }

    leaderboard = response['leaderboard']

    context = {
        'username': response['nick'],
        'id': response['userid'],
        'clan': {
            'clan_id': response.get('clanId', 0),
            'clan_role': response.get('clanMemberRole', 0),
            'clan_tag': response.get('clanName', 0),
        },
        'data': {
            'last_day': response['lastDay'],
            'register_day': response['registerDay'],
            'exp': response['exp'],
            'penalty_status': response['penaltyStatus']
        },
        'stats': {
            'air': {
                'rb': {
                    'current': extract_air_stats(leaderboard['air_realistic']['value_total']),
                    'month': extract_air_stats(leaderboard['air_realistic']['value_inhistory'])
                },
                'sb': {
                    'current': extract_air_stats(leaderboard['air_simulation']['value_total']),
                    'month': extract_air_stats(leaderboard['air_simulation']['value_inhistory'])
                },
                'ab': {
                    'current': extract_air_stats(leaderboard['air_arcade']['value_total']),
                    'month': extract_air_stats(leaderboard['air_arcade']['value_inhistory'])
                }
            },
            'ground': {
                'rb': {
                    'current': extract_tank_stats(leaderboard['tank_realistic']['value_total']),
                    'month': extract_tank_stats(leaderboard['tank_realistic']['value_inhistory'])
                },
                'sb': {
                    'current': extract_tank_stats(leaderboard['tank_simulation']['value_total']),
                    'month': extract_tank_stats(leaderboard['tank_simulation']['value_inhistory'])
                },
                'ab': {
                    'current': extract_tank_stats(leaderboard['tank_arcade']['value_total']),
                    'month': extract_tank_stats(leaderboard['tank_arcade']['value_inhistory'])
                }
            }
        }
    }

    return context
