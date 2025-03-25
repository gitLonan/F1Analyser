import pandas as pd
import json

class DriversApi:
    def get_last_race_drivers(raw_json: json):
        for driver in raw_json:
            print(driver['full_name'], driver['driver_number'])
        df = pd.read_json('data/cached.json')
        print(df.to_string())
        return df

