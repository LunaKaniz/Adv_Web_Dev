from django.urls import path
from .views import (
    ClimateListCreateView,
    ClimateFilterByDateStation,
    MonthlyAverages,
    Extremes,
    DeleteOldRecords
)

urlpatterns = [
    path('climate/', ClimateListCreateView.as_view()),
    path('climate/filter/', ClimateFilterByDateStation.as_view()),
    path('climate/averages/', MonthlyAverages.as_view()),
    path('climate/extremes/', Extremes.as_view()),
    path('climate/delete-old/', DeleteOldRecords.as_view()),
]
