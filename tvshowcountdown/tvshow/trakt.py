import requests
from django.conf import settings

from datetime import datetime, timezone
import dateutil.parser

headers = {
    'trakt-api-version': '2',
    'trakt-api-key': settings.TRAKT_API_KEY
}

TRAKT_URL = 'https://api-v2launch.trakt.tv/'


def search(search_term, type='show', year=None):
    '''
    :param str search_term: (required) the term to search trakt with
    :param str type: which type of program to search for. defaults to 'show'
    :param int year: limit search to this year
    :returns: list of results
    '''

    url = TRAKT_URL + 'search?query={}&type={}'.format(search_term, type)
    if year:
        year = int(year)
        url += '&year={}'.format(year)
    r = requests.get(url, headers=headers)
    result = []
    for i in r.json():
        result.append({
            'name': i['show']['title'],
            'year': i['show']['year'],
            'id': i['show']['ids']['trakt'],
            'slug': i['show']['ids']['slug']})
    return result


def get_seasons(show):
    '''
    :param str show: (required) show slug or trakt id
    :returns: details of the seasons
    '''
    url = TRAKT_URL + 'shows/{}/seasons?extended=full'.format(show)
    r = requests.get(url, headers=headers)
    result = []
    for i in r.json():
        result.append({
            'number': i['number'],
            'id': i['ids']['trakt'],
            'episode_count': i['episode_count'],
            'aired_episodes': i['aired_episodes'],
            })

    return result


def get_show(show):
    url = TRAKT_URL + 'shows/{}'.format(show)
    r = requests.get(url, headers=headers)
    return r.json()


def get_episode(show, season, episode):
    url = TRAKT_URL + 'shows/{}/seasons/{}/episodes/{}?extended=full'.format(
        show, season, episode)
    r = requests.get(url, headers=headers)
    try:
        r.raise_for_status()
    except:
        return None
    return r.json()


def get_next_episode(show):
    '''
    :param str show: (required) show slug or trakt id
    :returns: the next episode to be aired
    '''
    #episode = None
    seasons = get_seasons(show)
    seasons = sorted(seasons, key=lambda x: x['number'])
    last_episode = get_episode(show, seasons[-1]['number'], seasons[-1]['episode_count'])
    time_now = datetime.now(timezone.utc)
    if last_episode:
        try:
            last_episode_time = dateutil.parser.parse(last_episode['first_aired'])
            if last_episode_time < time_now:
                return None
        except:
            pass
    for season in seasons:
        last_season_episode = get_episode(show, season['number'], season['episode_count'])

        try:
            last_season_episode_time = dateutil.parser.parse(last_season_episode['first_aired'])
            if last_season_episode_time < time_now:
                continue
        except:
            continue
        
        for i in range(season['aired_episodes'], season['episode_count'] + 1):
            current_episode = get_episode(show, season['number'], i)
            try:
                current_episode_time = dateutil.parser.parse(current_episode['first_aired'])
            except:
                continue
            if current_episode_time > time_now:
                return current_episode
    return None
