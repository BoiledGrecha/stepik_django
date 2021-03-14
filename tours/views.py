from django.shortcuts import render, redirect
from django.http import HttpResponse
from data import (tours, departures,
                    title as title_main,
                    subtitle as subtitle_main,
                    description as description_main)
from random import sample

for i in tours:
    tours[i]["real_stars"] = int(tours[i]["stars"]) * "★"


def main_view(request):
    random_length = 6
    context = {"main_card": {"title": title_main,
                             "subtitle": subtitle_main,
                             "description": description_main}}

    tour_keys = list(tours.keys())
    if len(tour_keys) < 6:
        random_length = len(tour_keys)
    tour_keys = sample(tour_keys, k=random_length)
    random_tours = dict()
    for i in tour_keys:
        random_tours[i] = tours[i]
        random_tours[i]["short_description"] = random_tours[i].get("short_description", random_tours[i]["description"].split(".")[0] + ".")
    context["tours"] = random_tours

    return render(request, "tours/index.html", context)


def departure_view(request, departure):
    return render(request, "tours/departure.html")


def tour_view(request, tour_id):
    if tours.get(tour_id, -1) == -1:
        return HttpResponse('This tour doesnt exist', status=404)
    departure = departures[tours[tour_id]["departure"]]
    context = {"tour": tours[tour_id], "departure": departure}
    return render(request, "tours/tour.html", context)


def error_handler500(request, *args, **kwargs):
    return HttpResponse('Something is going wrong, please contact us +7 800 555 35 35 ', status=500)


def error_handler404(request, *args, **kwargs):
    return HttpResponse('You are trying to access unknown page', status=404)
