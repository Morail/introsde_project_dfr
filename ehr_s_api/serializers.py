# serializers.py'id'
from rest_framework import serializers
from .models import Patient, PatientDisease, Drug, Prescription, Disease, Measurement


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'uuid', 'last_name', 'first_name', 'tax_code', 'birth_date', 'entry_date', 'expiry_date',)


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ('id', 'name', 'substance_name', 'product_type', 'brand_name', 'dosage_form',)


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ('id', 'patient', 'drug', 'date', 'note',)

    def to_representation(self, instance):
        self.fields['patient'] = PatientSerializer(read_only=True)
        self.fields['drug'] = DrugSerializer(read_only=True)
        return super(PrescriptionSerializer, self).to_representation(instance)


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'patient', 'type', 'value', 'unit', 'note', 'date')

    def to_representation(self, instance):
        self.fields['patient'] = PatientSerializer(read_only=True)
        return super(MeasurementSerializer, self).to_representation(instance)


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ('id', 'name', 'icd_code',)


class PatientDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDisease
        fields = ('patient', 'disease', 'start_date', 'end_date',)

    def to_representation(self, instance):
        self.fields['patient'] = PatientSerializer(read_only=True)
        self.fields['disease'] = DiseaseSerializer(read_only=True)
        return super(PatientDiseaseSerializer, self).to_representation(instance)
