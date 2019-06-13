pip inimport factory

from apps.catalog.models import HazardousMaterial


class HazardousMaterialFactory(factory.DjangoModelFactory):
    kind = "Flammable liquid"
    coefficient = 1

    class Meta:
        model = HazardousMaterial
