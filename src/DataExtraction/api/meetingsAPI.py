import json
import pandas as pd

class MeetingApi:
    def extract_tracks(json_data: json) -> json:
        my_json = []
        dic = {}
        for track in json_data:
            dic["grand_prix"] = track["meeting_name"]
            dic["meeting_key"] = track["meeting_key"]
            my_json.append(dic)
            dic = {}
        return my_json

    def extract_tracks_data(json_data: json) -> json:
        my_json = []
        dic = {}
        for track in json_data:
            dic["year"] = track["year"]
            dic["date"] = track["date_start"]
            dic["meeting_key"] = track["meeting_key"]
            dic["location"] = track["location"]
            dic["country_name"] = track["country_name"]
            dic["grand_prix"] = track["meeting_name"]
            my_json.append(dic)
            dic = {}
        return my_json