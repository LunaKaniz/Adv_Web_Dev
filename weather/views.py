from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import ClimateRecord
from .serializers import ClimateRecordSerializer
from django.db.models import Avg, Q

class ClimateListCreateView(generics.ListCreateAPIView):
    queryset = ClimateRecord.objects.all()
    serializer_class = ClimateRecordSerializer

class ClimateFilterByDateStation(views.APIView):
    def get(self, request):
        station = request.query_params.get('station_id')
        date = request.query_params.get('date')
        records = ClimateRecord.objects.filter(station_id=station, date=date)
        serializer = ClimateRecordSerializer(records, many=True)
        return Response(serializer.data)

class MonthlyAverages(views.APIView):
    def get(self, request):
        station = request.query_params.get('station_id')
        month = int(request.query_params.get('month'))
        queryset = ClimateRecord.objects.filter(station_id=station, date__month=month)
        result = queryset.aggregate(
            avg_tmax=Avg('tmax'),
            avg_tmin=Avg('tmin'),
            avg_precip=Avg('precipitation')
        )
        return Response(result)

class Extremes(views.APIView):
    def get(self, request):
        records = ClimateRecord.objects.filter(Q(tmax__gte=35) | Q(precipitation__gte=50))
        serializer = ClimateRecordSerializer(records, many=True)
        return Response(serializer.data)

class DeleteOldRecords(views.APIView):
    def delete(self, request):
        before = request.query_params.get('before')
        count, _ = ClimateRecord.objects.filter(date__lt=before).delete()
        return Response({'deleted': count}, status=status.HTTP_200_OK)
