# serializers.py'id'
from rest_framework import serializers
from .models import Patient, PatientDisease, Drug, Prescription, Disease, Measurement


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['patient'] = PatientSerializer(read_only=True)
        self.fields['drug'] = DrugSerializer(read_only=True)
        return super(PrescriptionSerializer, self).to_representation(instance)


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['patient'] = PatientSerializer(read_only=True)
        return super(MeasurementSerializer, self).to_representation(instance)


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class PatientDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDisease
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['patient'] = PatientSerializer(read_only=True)
        self.fields['disease'] = DiseaseSerializer(read_only=True)
        return super(PatientDiseaseSerializer, self).to_representation(instance)
