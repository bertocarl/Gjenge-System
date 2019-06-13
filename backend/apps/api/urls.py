from django.urls import path

from apps.api.views import list_active_transportation, transportation_control, receive_transportation_tx, \
    finalize_transportation

app_name = 'api'

urlpatterns = [
    path('transportation/', list_active_transportation, name='list-active-transportation'),
    path('transportation/control/', transportation_control, name='transportation-control'),
    path('transportation/start_running/', receive_transportation_tx, name='receive-transportation-tx'),
    path('transportation/finalize/', finalize_transportation, name='finalize-transportation'),
]
