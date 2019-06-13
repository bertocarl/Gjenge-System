import secrets
import string
import requests

from django.conf import settings
from django.contrib.gis.geos import Point
from django.db import transaction


def generate_seed(length=32):
    chars = string.ascii_uppercase + "9"
    return ''.join(secrets.choice(chars) for i in range(length))


def get_first_root(seed, key):
    params = {
        'seed': seed,
        'key': key
    }
    response = requests.get(
        settings.LOCAL_NODE_SERVER + 'api/root/', params=params
    )
    if response.status_code == 200:
        return response.json()['root'], response.json()['key_trytes']

    return


@transaction.atomic
def fetch_messages_from_iota(transportation_id):
    from apps.api.models import Transportation, Checkpoint

    transportation = Transportation.objects.get(id=transportation_id)
    params = {
        'root': transportation.last_root or transportation.first_root,
        'key': transportation.key,
    }
    response = requests.get(
        settings.LOCAL_NODE_SERVER + 'api/messages/', params=params
    )
    payload = response.json()
    if payload.get('success'):
        last_root = payload.get('last_root')
        for message in payload.get('messages'):
            lt, lg = message.get('gps').split('+')
            _, _ = Checkpoint.objects.get_or_create(
                transportation=transportation,
                location=Point(float(lg), float(lt)),
                data=message,
            )
        transportation.last_root = last_root
        transportation.save()
    return


def calculate_distance(lat1, lon1, lat2, lon2):
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    r = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = r * c
    return distance


def get_critical_parameters(data):
    if data.get('temperature', 0) > 150:
        return True
    if data.get('gas', 0) > 10:
        return True
    return False
