from django.core.management.base import BaseCommand
import pandas as pd
from datetime import datetime
from weather.models import ClimateRecord

class Command(BaseCommand):
    help = 'Load climate data from CSV'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('weather_prediction_dataset.csv')

        # Convert DATE (e.g., 20000101) to proper datetime.date object
        df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')

        records = [
            ClimateRecord(
                station_id='BASEL',  # Or use something dynamic if needed
                date=row['DATE'].date(),
                tmax=row.get('BASEL_ter'),  # Max temp
                tmin=row.get('BASEL_hu'),   # Humidity (placeholder for min temp)
                precipitation=row.get('BASEL_pre')  # Precipitation
            )
            for _, row in df.iterrows()
        ]

        ClimateRecord.objects.bulk_create(records, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'✅ Loaded {len(records)} records.'))
