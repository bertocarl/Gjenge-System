from celery import app

from apps.api.utils import fetch_messages_from_iota


@app.shared_task()
def fetch_checkpoints_from_iota():
    from apps.api.models import Transportation
    for transportation in Transportation.objects.filter(status=Transportation.STATUS_ACTIVE):
        fetch_messages_from_iota(transportation.id)
