# -*- encoding: utf-8 -*-

from dal import autocomplete

from dal_admin_filters import Select2QuerySetView
from .models import City
from .models import Country


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Country.objects.none()
        qs = Country.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class CityAutocomplete(Select2QuerySetView):
    queryset = City.objects.all()
    fields = ('name',)
