import json

class JsonHandling:
    def extracting_json(data: str) -> json:
        """Extracting json part of the Http get request, disregarding header"""
        parts = data.split("\r\n\r\n", 1)
        json_part = parts[1].strip()
        json_response = json.loads(json_part)
        return json_response
    
    def pretty_json(ugly_json: json) -> json:
        return json.dumps(ugly_json, indent=4)