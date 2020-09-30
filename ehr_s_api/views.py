import time

import requests
from django.conf.urls import url
from django.http.response import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

# Create your views here.
from rest_framework.views import APIView

from .serializers import *
from .models import Patient, PatientDisease, Drug, Prescription, Disease, Measurement


class PatientList(viewsets.ModelViewSet):

    queryset = Patient.objects.all().order_by('id')
    serializer_class = PatientSerializer
    parser_classes = [JSONParser]
    filter_fields = ('first_name', 'last_name', 'tax_code')

    @action(detail=True)
    def prescriptions(self, request, pk=None):
        """
        Returns a list of all the prescriptions for the given user
        """
        user = self.get_object()
        queryset = Prescription.objects.all()
        queryset = queryset.filter(patient__id=pk)
        serializer = PrescriptionSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def diseases(self, request, pk=None):
        """
        Returns a list of all the diseases for the given user
        """
        user = self.get_object()
        queryset = PatientDiseaseSerializer.objects.all()
        queryset = queryset.filter(patient__id=pk)
        serializer = PatientDiseaseSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def measurements(self, request, pk=None):
        """
        Returns a list of all the measurements for the given user
        """
        user = self.get_object()
        queryset = Measurement.objects.all()
        queryset = queryset.filter(patient__id=pk)
        serializer = MeasurementSerializer(queryset, many=True)
        return Response(serializer.data)


class PrescriptionList(viewsets.ModelViewSet):
    """
    Return a list of all the existing prescriptions.
    """
    queryset = Prescription.objects.all().order_by('id')
    serializer_class = PrescriptionSerializer


class DrugList(viewsets.ModelViewSet):
    """
    Return a list of all the existing drugs.
    """
    queryset = Drug.objects.all().order_by('id')
    serializer_class = DrugSerializer

    def get_queryset(self):
        queryset = Drug.objects.all()

        # name
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        # substance_name
        s_name = self.request.query_params.get('substance_name', None)
        if s_name is not None:
            queryset = queryset.filter(substance_name=s_name)

        precautions = 'PIPPO'

        return queryset

    """
    List results retrieved from api.fda.gov.
    """

    @action(detail=True)
    def openfda(self, request, pk=None):
        """
        Returns a list of all the measurements for the given user
        """
        drug = self.get_object()
        base_uri = 'https://api.fda.gov:443/drug/label.json'
        search_string = 'openfda.generic_name:"' + drug.substance_name + '"+AND+openfda.brand_name:"' + drug.brand_name + '"'
        query_string = '%s?%s=%s&%s=%d' % (base_uri, 'search', search_string, 'limit', 1)

        attempt_num = 0  # keep track of how many times we've retried
        while attempt_num < 2:
            r = requests.get(
                query_string,
                timeout=10)
            if r.status_code == 200:
                data = r.json()
                return Response(data, status=status.HTTP_200_OK)
            else:
                attempt_num += 1
                # You can probably use a logger to log the error here
                time.sleep(5)  # Wait for 5 seconds before re-trying
        return Response({"error": "Request failed - " + query_string}, status=r.status_code)

    def create(self, request, format=None):

        search_string = 'openfda.generic_name:"' + request.data.get(
            'substance_name') + '"+AND+openfda.brand_name:"' + request.data.get('brand_name') + '"'

        res = OpenFDAView(search_string)

        manufacter_name = ""
        precautions= ""
        drug_interactions = ""

        if res is not None:

            try:
                manufacter_name = res['results'][0]['openfda']['manufacturer_name'][0]
            except:
                print('Error!')
            try:
                precautions = str(res['results'][0]['precautions'][0])[:4999]
            except:
                print('Error!')
            try:
                drug_interactions = str(res['results'][0]['drug_interactions'][0])[:4999]
            except:
                print('Error!')

            request.data.update({"manufacter_name": manufacter_name,
                                 'precautions': precautions,
                                 'drug_interactions': drug_interactions
                                })

        serializer = DrugSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDiseaseList(viewsets.ModelViewSet):
    queryset = PatientDisease.objects.all().order_by('id')
    serializer_class = PatientDiseaseSerializer
    filter_fields = ['disease__name', 'start_date']

    def post(self, request, format=None):
        serializer = PatientDisease(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeasurementList(viewsets.ModelViewSet):
    queryset = Measurement.objects.all().order_by('id')
    serializer_class = MeasurementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'date']

    def get_queryset(self):
        queryset = Measurement.objects.all()

        # type
        type = self.request.query_params.get('type', None)
        if type is not None:
            queryset = queryset.filter(type=type)

        # dateFrom
        date_from = self.request.query_params.get('dateFrom', None)
        if date_from is not None:
            queryset = queryset.filter(date__lt=date_from)

        return queryset

    def post(self, request, format=None):
        serializer = Measurement(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def OpenFDAView(search_string, MAX_ATTEMPT=2):
    """
    Query the OpenFDA API for drugs records
    """
    base_uri = 'https://api.fda.gov:443/drug/label.json'
    query_string = '%s?%s=%s&%s=%d' % (base_uri, 'search', search_string, 'limit', 1)

    attempt_num = 0  # keep track of how many times we've retried
    res = None
    while attempt_num < MAX_ATTEMPT and res is None:
        r = requests.get(
            query_string,
            timeout=10)
        if r.status_code == 200:
            res = r.json()
        else:
            attempt_num += 1
            # You can probably use a logger to log the error here
            time.sleep(2)  # Wait for 5 seconds before re-trying

    return res
