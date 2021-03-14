from django.shortcuts import render
from django.http import HttpResponse
from data import (tours, departures,
                  title as title_main,
                  subtitle as subtitle_main,
                  description as description_main)
from random import sample

for i in tours:
    tours[i]["real_stars"] = tours[i].get("real_stars", int(tours[i]["stars"]) * "★")
    tours[i]["short_description"] = tours[i].get("short_description", tours[i]["description"].split(".")[0] + ".")


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
    context["tours"] = random_tours
    context["header"] = departures

    return render(request, "tours/index.html", context)


def departure_view(request, departure):
    container_header = dict()
    container_header["from"] = departures.get(departure)
    if not container_header["from"]:
        return HttpResponse('City doesnt exist', status=404)
    container_header["from"] = container_header["from"][0].lower() + container_header["from"][1:]
    tours_from_city = dict()
    context = dict()
    max_nights, min_nights, max_price, min_price = 0, 0, 0, 0
    for i in tours.keys():
        if tours[i].get("departure", "") == departure:
            tours_from_city[i] = tours[i]
            if tours[i]["nights"] > max_nights:
                max_nights = tours[i]["nights"]
            if tours[i]["price"] > max_price:
                max_price = tours[i]["price"]
            if min_nights == 0 or tours[i]["nights"] < min_nights:
                min_nights = tours[i]["nights"]
            if min_price == 0 or tours[i]["price"] < min_price:
                min_price = tours[i]["price"]

    if not tours_from_city:
        container_header["info"] = "Найдено 0 туров."
    else:
        container_header["info"] = """Найдено {} туров,
                                    от {} до {} и от {} ночей до {} ночей
                                    """.format(len(tours_from_city),
                                               min_price, max_price,
                                               min_nights, max_nights)
    context["tours"] = tours_from_city
    context["container_header"] = container_header
    context["header"] = departures
    return render(request, "tours/departure.html", context)


def tour_view(request, tour_id):
    if tours.get(tour_id, -1) == -1:
        return HttpResponse('This tour doesnt exist', status=404)
    departure = departures[tours[tour_id]["departure"]]
    context = {"tour": tours[tour_id], "departure": departure}
    context["header"] = departures
    return render(request, "tours/tour.html", context)


def error_handler500(request, *args, **kwargs):
    return HttpResponse('Something is going wrong, please contact us +7 800 555 35 35 ', status=500)


def error_handler404(request, *args, **kwargs):
    return HttpResponse('You are trying to access unknown page', status=404)
