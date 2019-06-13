import json

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404

from apps.api import serializers
from apps.api.models import Device, Transportation, Checkpoint, UserProfile
from apps.api.serializers import CheckpointSerializer
from apps.api.utils import get_critical_parameters


@csrf_exempt
def transportation_control(request):
    request_data = json.loads(request.body)

    try:
        device = Device.objects.get(uuid=request_data.get('device_id'))
    except Device.DoesNotExist:
        return JsonResponse({
            'success': False
        })

    transportation_id = request_data.get('transportation_id')
    transportation = Transportation.objects.filter(
        device=device, status=Transportation.STATUS_ACTIVE
    )
    payload = {
        'success': True,
        'state': {}
    }
    if transportation.exists():
        transportation = transportation.get()
        payload['state']['transportation_id'] = transportation.id
        if transportation_id != transportation.id:
            payload['state']['seed'] = transportation.seed
            payload['state']['key'] = transportation.key

    return JsonResponse(payload)


def list_active_transportation(request):
    payload = {}
    transportation = Transportation.objects.filter(status=Transportation.STATUS_ACTIVE).order_by('-id')
    if transportation.exists():
        serializer = serializers.TransportationSerializer(transportation, many=True)
        transportation_data = serializer.data
        for transportation in transportation_data:
            checkpoints = []
            for checkpoint in transportation['checkpoint_set']:
                checkpoint = Checkpoint.objects.get(id=checkpoint)
                checkpoint_data = CheckpointSerializer(checkpoint).data
                checkpoint_data['is_critical'] = get_critical_parameters(checkpoint_data.get('data'))
                checkpoints.append(checkpoint_data)
            checkpoints.reverse()
            transportation['checkpoint_set'] = checkpoints
            user = Transportation.objects.get(id=transportation['id']).device.user
            transportation['user_phone'] = UserProfile.objects.get(user=user).phone
        payload.update({
            'transportations': transportation_data
        })

    return JsonResponse(payload)


@csrf_exempt
@transaction.atomic
def receive_transportation_tx(request):
    transportation = get_object_or_404(Transportation, id=request.POST.get('transportation_id'))
    transportation.status = Transportation.STATUS_ACTIVE
    transportation.save()

    return JsonResponse({'success': True})


@csrf_exempt
@transaction.atomic
def finalize_transportation(request):
    transportation = get_object_or_404(Transportation, id=request.POST.get('transportation_id'))
    is_able_to_finish = transportation.finish()
    if is_able_to_finish:
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
