from django.db import models


class HazardousMaterial(models.Model):
    kind = models.CharField(max_length=255)
    coefficient = models.FloatField()
    repercussion = models.TextField()

    def __str__(self):
        return self.kind
