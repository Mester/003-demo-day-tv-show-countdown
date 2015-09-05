from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from . import trakt

def index(request):
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
    return render_to_response('index.html', context)

def countdown(request, slug_id):
    context = {}
    # TODO: Get actual time to next episode
    time_later = trakt.get_next_episode(slug_id)
    if time_later == None:
        context["error_message"] = "Could not get next episode"
    else:
        countdown_timer = {}
        countdown_timer["year"] = time_later.year
        countdown_timer["month"] = time_later.month - 1 # Because js counts months from 0
        countdown_timer["day"] = time_later.day
        countdown_timer["hour"] = time_later.hour
        countdown_timer["minute"] = time_later.minute
        countdown_timer["second"] = time_later.second
        context["countdown_timer"] = countdown_timer
    return render_to_response('index.html', context)