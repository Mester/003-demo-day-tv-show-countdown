from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from . import trakt

import dateutil.parser


def search(request):
    context = {}
    if "search_term" in request.GET:
        return handle_search(request)
    return render_to_response('index.html', context)


def handle_search(request):
    context = {}
    if request.GET["search_term"] == "":
        context["error_message"] = "Can't search with an empty field."
    else:
        context["search_results"] = trakt.search(request.GET["search_term"])
        context["search_term"] = request.GET["search_term"]

    if request.GET.get("add_show", None) is not None:
        user_shows = request.session.get("user_shows", None)
        if user_shows:
            user_shows = user_shows.split(',')
            show_to_add = request.GET["add_show"]
            if show_to_add not in user_shows:
                user_shows.append(show_to_add)
                context["success_message"] = "Added {} to your collection".format(show_to_add)
            else:
                context["warning_message"] = "You already have {} in your collection".format(show_to_add)
            user_shows = ','.join(user_shows)
        else:
            user_shows = request.GET["add_show"]

        request.session["user_shows"] = user_shows
    return render_to_response('index.html', context)


def info(request, slug_id):
    context = {}
    episode = trakt.get_next_episode(slug_id)
    show = trakt.get_show(slug_id)
    if episode == None or episode['first_aired'] is None:
        context["error_message"] = "Could not get next episode"
    else:
        timestamp = episode['first_aired']
        time_later = dateutil.parser.parse(timestamp)
        countdown_timer = {}
        countdown_timer["year"] = time_later.year
        countdown_timer["month"] = time_later.month - 1 # Because js counts months from 0
        countdown_timer["day"] = time_later.day
        countdown_timer["hour"] = time_later.hour
        countdown_timer["minute"] = time_later.minute
        countdown_timer["second"] = time_later.second
        context["countdown_timer"] = countdown_timer
        show_info = {}
        show_info["episode_title"] = episode["title"]
        show_info["season"] = episode["season"]
        show_info["episode_number"] = episode["number"]
        show_info["show_title"] = show["title"]
        context["show_info"] = show_info
    return render_to_response('info.html', context)


def shows(request):
    context = {}
    user_shows = request.session.get("user_shows", None)
    if user_shows:
        user_shows = user_shows.split(',')
        users_shows = []
        for show in user_shows:
            users_shows.append(trakt.get_show(show))
        context['users_shows'] = users_shows
    return render_to_response('shows.html', context)
