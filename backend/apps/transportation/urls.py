from django.urls import path

from apps.transportation.views import TransportationListView

urlpatterns = [
    path('list/', TransportationListView.as_view(), name='transportation-list'),
]
