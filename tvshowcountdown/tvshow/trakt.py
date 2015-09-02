import requests
from django.conf import settings


headers = {
    'trakt-api-version': '2',
    'trakt-api-key': settings.TRAKT_API_KEY
}


def search(search_term, type='show', year=None):
    '''
    :param str search_term: (required) the term to search trakt with
    :param str type: which type of program to search for. defaults to 'show'
    :param int year: limit search to this year
    :returns: list of results
    '''

    url = 'https://api-v2launch.trakt.tv/search?query={}&type={}'.format(search_term, type)
    if year:
        year = int(year)
        url += '&year={}'.format(year)
    r = requests.get(url, headers=headers)
    result = []
    for i in r.json():
        result.append({
            'name': i['show']['title'],
            'year': i['show']['year'],
            'slug': i['show']['ids']['slug']})
    return result
