#my class imports


import json
import os
import polars as pl


class Stint:


    @staticmethod
    def fastest_lap():
        dir_path_content = f"data/cached"

    @staticmethod
    def get_df_stints(session: str) -> pl.DataFrame:
        df_s = []
        json_list = os.listdir(f"data/cached_calls/stints/{session}")
        for file in json_list:
            path = f"data/cached_calls/stints/{session}/{file}"
            df = pl.DataFrame(json.load(open(path)))
            df_s.append(df)
        df_stints = pl.concat(df_s, how="vertical") 
        return df_stints