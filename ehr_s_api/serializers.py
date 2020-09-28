# serializers.py'id'
from rest_framework import serializers
from .models import Patient, PatientDisease, Drug, Prescription, Disease, Measurement


class PatientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Patient
        fields = ('id', 'uuid', 'last_name', 'first_name', 'tax_code', 'birth_date', 'entry_date', 'expiry_date', )


class DrugSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drug
        fields = ('id', 'name', 'substance_name', 'product_type', 'brand_name', 'dosage_form',)


class PrescriptionSerializer(serializers.HyperlinkedModelSerializer):
    patient = PatientSerializer()
    drug = DrugSerializer()

    class Meta:
        model = Prescription
        fields = ('id', 'patient', 'drug', 'start_date', 'end_date', 'note',)


class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Measurement
        fields = ('id', 'patient', 'type', 'value', 'unit')


class DiseaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Disease
        fields = ('id', 'name', 'icd_code',)


class PatientDiseaseSerializer(serializers.HyperlinkedModelSerializer):
    patient = PatientSerializer()
    disease = DiseaseSerializer()

    class Meta:
        model = PatientDisease
        fields = ('patient', 'disease', 'start_date', 'end_date', )



