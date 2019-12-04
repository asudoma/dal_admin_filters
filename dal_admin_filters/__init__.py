# -*- encoding: utf-8 -*-
from dal import autocomplete
from django import forms
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.utils import get_fields_from_path
from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import Media, MEDIA_TYPES

from .views import Select2QuerySetView


class AutocompleteFilter(SimpleListFilter):
    template = "dal_admin_filters/autocomplete-filter.html"
    title = ''
    field_name = ''
    field_pk = 'id'
    autocomplete_url = ''
    placeholder_prefix = ''
    is_placeholder_title = True
    widget_attrs = {}

    class Media:
        css = {
            'all': (
                'dal_admin_filters/css/select2.min.css',
                'autocomplete_light/select2.css',
                'dal_admin_filters/css/autocomplete-fix.css'
            )
        }
        js = (
            'admin/js/jquery.init.js',
            'autocomplete_light/jquery.init.js',
            'dal_admin_filters/js/select2.full.min.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'dal_admin_filters/js/querystring.js',
        )

    def __init__(self, request, params, model, model_admin):
        super(AutocompleteFilter, self).__init__(request, params, model, model_admin)
        self.lookup_kwarg = '{}__id__exact'.format(self.parameter_name)

        self._add_media(model_admin)

        field = forms.ModelChoiceField(
            queryset=self.get_queryset_for_field(model, self.parameter_name),
            widget=autocomplete.ModelSelect2(
                url=self.get_autocomplete_url(request),
            )
        )

        attrs = self.widget_attrs.copy()
        attrs['id'] = 'id-%s-dal-filter' % self.lookup_kwarg
        if self.is_placeholder_title:
            attrs['data-placeholder'] = self.placeholder_prefix + self.title
        self.rendered_widget = field.widget.render(
            name=self.parameter_name,
            value=self.used_parameters.get(self.parameter_name, ''),
            attrs=attrs
        )

    def get_queryset_for_field(self, model, field_path):
        field = get_fields_from_path(model, field_path)[-1]
        return field.related_model.objects.all()

    def _add_media(self, model_admin):

        if not hasattr(model_admin, 'Media'):
            raise ImproperlyConfigured('Add empty Media class to %s. Sorry about this bug.' % model_admin)

        def _get_media(obj):
            return Media(media=getattr(obj, 'Media', None))

        media = _get_media(model_admin) + _get_media(AutocompleteFilter) + _get_media(self)

        for name in MEDIA_TYPES:
            setattr(model_admin.Media, name, getattr(media, "_" + name))

    def get_autocomplete_url(self, request):
        return self.autocomplete_url

    def has_output(self):
        return True

    def lookups(self, request, model_admin):
        return ()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.parameter_name: self.value()})
        else:
            return queryset
