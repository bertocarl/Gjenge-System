from django.conf import settings
from django.views.generic import TemplateView

from apps.api.models import Transportation


class TransportationListView(TemplateView):
    template_name = 'transportation/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['transportations'] = Transportation.objects.all().order_by('-id')
        return context
