from django.utils import timezone

from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class ParanoidQuerySet(QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.
    """

    def delete(self):
        for obj in self:
            obj.deleted_on = timezone.now()
            obj.save()


class ParanoidManager(models.Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """

    def get_queryset(self):
        return ParanoidQuerySet(self.model, using=self._db).filter(
            deleted_on__isnull=True)


class ParanoidModel(models.Model):
    class Meta:
        abstract = True

    deleted_on = models.DateTimeField(null=True, blank=True)
    objects = ParanoidManager()
    original_objects = models.Manager()

    def delete(self):
        print("HURRAH!")
        self.deleted_on = timezone.now()
        self.save()


class Patient(ParanoidModel):
    uuid = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    tax_code = models.CharField(max_length=16)
    birth_date = models.DateField()
    entry_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return '[%d] %s %s %s' % (self.id, self.tax_code, self.last_name, self.first_name,)


class Measurement(ParanoidModel):

    class TypeOfMeasurement(models.TextChoices):
        HEIGHT = 'Height', _('Height')
        WEIGHT = 'Weight', _('Weight')
        BLOOD_P = 'BloodPreassure', _('Blood preassure')
        GLICATA = 'Glicata', _('Glicata')
        OTHER = 'n.a.', _('Undefined')

    class UnitOfMeasurement(models.TextChoices):
        KILOGRAMS = 'Kg', _('Kilograms')
        CENTIMETERS = 'cm', _('Centimeters')
        MMHG = 'mmHg', _('Millimeters of Mercury')
        MG_DL = 'mg/dL', _('Millograms per deciliter')

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type = models.CharField(max_length=60,
                            choices=TypeOfMeasurement.choices,
                            default=TypeOfMeasurement.OTHER)
    value = models.CharField(max_length=60)
    unit = models.CharField(max_length=60,
                            choices=UnitOfMeasurement.choices,
                            default="",
                            null=True)
    date = models.DateTimeField()

    def __str__(self):
        return 'Measurement for patient id %d -> type: %s - value: %s' % (self.patient.id, self.type, self.value,)


class Disease(ParanoidModel):
    name = models.CharField(max_length=60)
    icd_code = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class PatientDisease(ParanoidModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.patient.id, self.disease.name,)


class Drug(ParanoidModel):
    name = models.CharField(max_length=60)
    substance_name = models.CharField(max_length=60)
    product_type = models.CharField(max_length=60)
    brand_name = models.CharField(max_length=60)
    dosage_form = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Prescription(ParanoidModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    diagnostic_question = models.CharField(max_length=2000, null=True)
    note = models.CharField(max_length=200)

    def __str__(self):
        return '%s - %s' % (self.patient.id, self.drug.name,)
