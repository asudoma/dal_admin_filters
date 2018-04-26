# -*- encoding: utf-8 -*-

from dal_admin_filters import Select2QuerySetView
from .models import City
from .models import Country


class CountryAutocomplete(Select2QuerySetView):
    queryset = Country.objects.all()
    fields = ('name',)


class CityAutocomplete(Select2QuerySetView):
    queryset = City.objects.all()
    fields = ('name',)
