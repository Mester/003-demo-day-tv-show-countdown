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
    # TODO: Get actual time
    context["countdown_timer"] = "7 Days 5 Hours 3 Minutes 56 Seconds"
    return render_to_response('index.html', context)