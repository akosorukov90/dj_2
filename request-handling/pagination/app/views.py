import csv
from urllib import parse

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    bus_stops = []
    with open(settings.BUS_STATION_CSV, newline='', encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bus_stops.append({'Name': row['Name'], 'Street': row['Street'], 'District': row['District']})
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(bus_stops, settings.POST_ON_PAGE)
    page = paginator.get_page(page_number)
    msg = page.object_list
    current_page = page_number
    if page_number < paginator.num_pages:
        params = {'page': page_number + 1}
        next_page_url = reverse(bus_stations) + '?' + parse.urlencode(params)
    else:
        next_page_url = None
    if page_number == 1:
        prev_page_url = None
    else:
        params = {'page': page_number - 1}
        prev_page_url = reverse(bus_stations) + '?' + parse.urlencode(params)
    return render(request, 'index.html', context={
        'bus_stations': msg,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

