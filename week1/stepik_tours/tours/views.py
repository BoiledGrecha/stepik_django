from django.shortcuts import render, redirect
# from django.http import HttpResponse


def main_view(request):
    return render(request, "index.html")


def departure_view(request, departure):
    return render(request, "departure.html")


def tour_view(request, id):
    return render(request, "tour.html")


def error_handler(request, *args, **kwargs):
    return redirect('/')
