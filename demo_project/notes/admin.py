from django.contrib import admin

from dal_admin_filters import AutocompleteFilter
from .models import Country, City, Person


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


class CountryFilter(AutocompleteFilter):
    title = 'Country from'
    parameter_name = 'city__country'
    autocomplete_url = 'country-autocomplete'
    is_placeholder_title = False


class CityFilter(AutocompleteFilter):
    title = 'City from'
    parameter_name = 'city'
    autocomplete_url = 'city-autocomplete'
    is_placeholder_title = False


class CityPlaceholderFilter(AutocompleteFilter):
    title = 'City from'
    autocomplete_url = 'city-autocomplete'
    is_placeholder_title = True


class CityCustomPlaceholderFilter(AutocompleteFilter):
    title = 'City from'
    parameter_name = 'city'
    autocomplete_url = 'city-autocomplete'
    widget_attrs = {
        'data-placeholder': 'Filter by city name'
    }


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_filter = [CountryFilter, CityFilter, 'first_name']

    class Media:
        pass
