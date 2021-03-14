from django.shortcuts import render, redirect
from django.http import HttpResponse

import data
# from django.http import HttpResponse


def main_view(request):
    return render(request, "tours/index.html")


def departure_view(request, departure):
    return render(request, "tours/departure.html")


def tour_view(request, tour_id):
    return render(request, "tours/tour.html")


def error_handler500(request, *args, **kwargs):
    return HttpResponse('Something is going wrong, please contact us +7 800 555 35 35 ', status=500)


def error_handler404(request, *args, **kwargs):
    return HttpResponse('You are trying to access unknown page', status=404)
