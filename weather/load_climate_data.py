import pandas as pd
from weather.models import ClimateRecord

def run():
    df = pd.read_csv('weather_prediction_dataset.csv', parse_dates=['date'])

    records = [
        ClimateRecord(
            station_id=row['station_id'],
            date=row['date'].date(),
            tmax=row.get('tmax'),
            tmin=row.get('tmin'),
            precipitation=row.get('precip')
        )
        for _, row in df.iterrows()
    ]

    ClimateRecord.objects.bulk_create(records, ignore_conflicts=True)
    print(f"Loaded {len(records)} records into the database.")
