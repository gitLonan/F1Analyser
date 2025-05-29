import json
import polars as pl


class SessionAPi:


    def extract_track_sessions(json_data: json) :
        pass

    def get_df_session(setparam: object):
        dir_path_content = f"data/cached_calls/sessions/meeting_{setparam.meeting_key}_tracks_data.json"

        with open(dir_path_content, "r") as file:
            tracks_json = json.load(file)
            df = pl.DataFrame(tracks_json)

        return df