from dal import autocomplete
from django.db.models import Q
from django.views.generic.list import MultipleObjectMixin


class Select2QuerySetView(autocomplete.Select2QuerySetView):
    fields = ()

    def get_queryset(self):
        qs = MultipleObjectMixin.get_queryset(self)
        if not self.is_allowed():
            return qs.none()
        if self.q:
            qs = self.filter_qs(qs)
        return qs

    def filter_qs(self, qs):
        if not getattr(self, 'fields', None):
            raise AttributeError('You must specify "fields" field '
                                 'or inherit "filter_qs" method')
        queries = [Q(**{'{}__istartswith'.format(item): self.q}) for item in self.fields]
        q = queries.pop()
        for item in queries:
            q |= item
        return qs.filter(q)

    def is_allowed(self):
        return True
