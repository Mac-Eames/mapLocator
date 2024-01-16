from django.shortcuts import render
from django.http import HttpResponse
import folium
import geocoder
from .models import Search
from .form import SearchForm

# Create your views here
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SearchForm()
    address = Search.objects.all().last() 
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    # To scrape out the not correctly spelled name of place
    if lat == None or lng == None:
        address.delete()
        return HttpResponse('Your input is invalid')
    # Create a map object
    m = folium.Map()
    # Adding a marker to the map
    folium.Marker([lat, lng], tooltip='Click for more', popup=country).add_to(m)
    # Get HTML representation of Map object
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'index.html', context)
