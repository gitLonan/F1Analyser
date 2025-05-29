import polars as pl
import os
import json

class LapsAPI:

    
    @staticmethod
    def get_df_laps(session: str) -> pl.DataFrame:
        df_s = []
        json_list = os.listdir(f"data/cached_calls/laps/{session}")
        for file in json_list:
            path = f"data/cached_calls/laps/{session}/{file}"
            df = pl.DataFrame(json.load(open(path)))
            df_s.append(df)
        df_laps = pl.concat(df_s, how="vertical") 
        return df_laps

    @staticmethod
    def get_single_df_laps(session: str, driver_number: int) -> pl.DataFrame:
        path = f"data/cached_calls/laps/{session}/driver_number_{driver_number}.json"  
        df = pl.DataFrame(json.load(open(path)))
        return df