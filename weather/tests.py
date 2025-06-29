from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import ClimateRecord
from datetime import date

class ClimateRecordTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.record = ClimateRecord.objects.create(
            station_id="BASEL",
            date=date(2023, 1, 1),
            tmax=30.5,
            tmin=15.0,
            precipitation=5.2
        )

    def test_get_all_records(self):
        response = self.client.get('/api/climate/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('station_id', response.json()[0])

    def test_filter_by_station_and_date(self):
        url = '/api/climate/filter/?station_id=BASEL&date=2023-01-01'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_monthly_averages(self):
        url = '/api/climate/averages/?station_id=BASEL&month=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('avg_tmax', response.json())

    def test_post_record(self):
        data = {
            "station_id": "BASEL",
            "date": "2023-02-01",
            "tmax": 28.0,
            "tmin": 14.0,
            "precipitation": 6.5
        }
        response = self.client.post('/api/climate/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['station_id'], 'BASEL')

    def test_extreme_weather(self):
        ClimateRecord.objects.create(
            station_id="BASEL",
            date=date(2023, 3, 1),
            tmax=40.0,
            precipitation=60.0
        )
        response = self.client.get('/api/climate/extremes/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_delete_old_records(self):
        url = '/api/climate/delete-old/?before=2023-02-01'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.json()['deleted'], 1)
