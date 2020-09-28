from django.http.response import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

# Create your views here.
from .serializers import PatientSerializer, PrescriptionSerializer, DrugSerializer, PatientDiseaseSerializer
from .models import Patient, PatientDisease, Drug, Prescription, Disease, Measurement


# class PatientViewSet(viewsets.ModelViewSet):
# queryset = Patient.objects.all().order_by('last_name')
# serializer_class = PatientSerializer
# filter_fields = ('first_name','last_name','tax_code')

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


class PrescriptionList(viewsets.ModelViewSet):
    """
    Return a list of all the existing prescriptions.
    """

    queryset = Prescription.objects.all().order_by('id')
    serializer_class = PrescriptionSerializer


class DrugList(viewsets.ModelViewSet):
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

        return queryset


class PatientDiseaseList(viewsets.ModelViewSet):
    queryset = PatientDisease.objects.all().order_by('id')
    serializer_class = PatientDiseaseSerializer

    def post(self, request, format=None):
        print(request)
        print(request.data)
        serializer = PatientDisease(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)