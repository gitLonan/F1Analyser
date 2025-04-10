import json


class MeetingApi:
    @staticmethod
    def extract_tracks(year: str, Setparam) -> json:
        """ Extracts tracks and their respected keys - key is a unique number """
        dir_path_content = f"data/cached_calls/tracks/year_{year}_tracks.json"
        track_list = []
        track_key_list = []
        with open(dir_path_content, "r") as file:
            tracks_json = json.load(file)
            for dic in tracks_json:
               track_list.append([dic["meeting_name"], dic["meeting_key"]])
               track_key_list.append(dic["meeting_key"])
            Setparam.set_meeting_key_list(track_key_list)
        return track_list
        
    @staticmethod
    def extract_track_sessions(json_data: json, Setparam) -> json:
        """ Extracts all the sessions that happend during the event(f1 weekend) """
        dir_path_content = f"data/cached_calls/sessions/session_{Setparam.meeting_key}_tracks_data.json"
        session_list = []
        session_key_list = []
        with open(dir_path_content, "r") as file:
            tracks_json = json.load(file)
            for dic in tracks_json: 
               session_list.append([dic["session_name"], dic["session_key"]])
               session_key_list.append(dic["session_key"])
            Setparam.set_session_key_list(session_key_list)
        return session_list
    