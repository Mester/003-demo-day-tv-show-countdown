from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from datetime import datetime

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
    time_now = datetime.now()
    # TODO: Get actual time to next episode
    time_later = datetime(2015, 9, 10, 23, 33, 56)
    time_until = time_later - time_now
    seconds = time_until.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days = time_until.days
    context["countdown_timer"] = {"days": days, "hours": hours, "minutes": minutes, "seconds": seconds}
    #context["countdown_timer"]["string_rep"] = str(time_until)
    return render_to_response('index.html', context)