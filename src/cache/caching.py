import json
from src.DataExtraction.jsonhandling import JsonHandling

class CacheAPI:
    def cache_tracks(json_data: json) -> None:
        with open("data/cachedCalls/tracks.json", "w") as file:
            pretty_json = JsonHandling.pretty_json(json_data)
            file.write(pretty_json)
            
    def cache_tracks_data(json_data: json) -> None:
        with open("data/cachedCalls/tracks_data.json", "w") as file:
            pretty_json = JsonHandling.pretty_json(json_data)
            file.write(pretty_json)