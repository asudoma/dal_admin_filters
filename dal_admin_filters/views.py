from dal import autocomplete
from django.db.models import Q


class Select2QuerySetView(autocomplete.Select2QuerySetView):
    limit_queryset = 10
    queryset = None
    fields = ()

    def get_queryset(self):
        if not getattr(self, 'queryset', None):
            raise AttributeError('You must specify "queryset" attribute '
                                 'or inherit "get_queryset" method')

        qs = self.queryset
        if not self.is_allowed():
            return qs.none()
        if self.q:
            qs = self.filter_qs(qs)
        else:
            return qs[:10]
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
        return self.request.user.is_authenticated() and self.request.user.is_staff
