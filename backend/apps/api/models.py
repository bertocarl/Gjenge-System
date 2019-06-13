import base64
import secrets
import uuid as uuid
from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models

from django.contrib.gis.db.models import PointField
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.api import utils
from apps.catalog.models import HazardousMaterial


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user}'s profile"


class Device(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Transportation(models.Model):
    STATUS_CREATED = 'created'
    STATUS_ACTIVE = 'active'
    STATUS_FINISHED = 'finished'
    STATUS_ARBITRAGE = 'arbitrage'
    STATUS_CHOICES = (
        (STATUS_CREATED, "Created"),
        (STATUS_ACTIVE, "Active"),
        (STATUS_FINISHED, "Finished"),
        (STATUS_ARBITRAGE, "Arbitrage"),
    )
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    start_point = PointField()
    end_point = PointField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seed = models.CharField(max_length=81, blank=True)
    key = models.CharField(max_length=81, blank=True)
    first_root = models.CharField(max_length=255, blank=True, null=True)
    last_root = models.CharField(max_length=255, blank=True, null=True)
    type_of_hazardous_material = models.ForeignKey(
        HazardousMaterial, on_delete=models.CASCADE, blank=True, null=True
    )
    volume = models.FloatField(blank=True, null=True, help_text="Volume in tons")
    distance = models.FloatField(blank=True, null=True, help_text="Distance in km")
    key_trytes = models.CharField(max_length=255, blank=True, null=True)

    risk_value = models.FloatField(blank=True, null=True)
    stake = models.FloatField(blank=True, null=True)
    tx_address = models.CharField(max_length=255, blank=True, null=True)

    data = JSONField(blank=True, null=True)

    @transaction.atomic
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.seed = utils.generate_seed()
            self.key = secrets.token_hex(40)
            self.first_root, self.key_trytes = utils.get_first_root(self.seed, self.key)
            self.risk_value = self.get_stake_for_transportation()
            self.stake = self.risk_value

        return super(Transportation, self).save(force_insert, force_update, using, update_fields)

    def get_stake_for_transportation(self):
        return (self.volume * self.distance * self.type_of_hazardous_material.coefficient) / 100

    def get_encrypted_payload(self):
        payload = {
            'start_point': f'{self.start_point[1]}+{self.start_point[0]}',
            'end_point': f'{self.end_point[1]}+{self.end_point[0]}',
        }
        payload = urlencode(payload)

        return base64.b64encode(payload.encode()).decode("utf-8")

    def check_finish(self):
        try:
            last_checkpoint = Checkpoint.objects.filter(transportation=self).order_by('-id')[0]
            distance = utils.calculate_distance(self.end_point[1], self.end_point[0], last_checkpoint.location[1],
                                                last_checkpoint.location[0])
            print("dist %s" % distance)
            if distance < 5:
                return True
        except IndexError:
            return False

    def finish(self):
        if self.check_finish():
            self.status = Transportation.STATUS_FINISHED
            self.save()
            return True

        return False


class Checkpoint(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    location = PointField()
    transportation = models.ForeignKey(Transportation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = JSONField(blank=True, null=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
