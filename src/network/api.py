#My classes
from src.network.http import HttpRequest
from src.network.errors.httpexception import HttpException
#My func
from urllib.parse import quote


from enum import Enum
import json

class API(Enum):
    DRIVERS = "/v1/drivers?"
    LAPS = "/v1/laps?"
    POSITION = "/v1/position?"
    STINTS = "/v1/stints?"

class ApiCommunication:

    def get_api(host: str, api: str =None,attributes: list[str]=[]) -> json:
        """ 
            Args:
                host (str) - websites domain name, example api.openf1.org
                api [str] - path to the resource on the hosts server, stored insde of API
                attributes - found on the site https://openf1.org/
            Returns:
                response_text (json) - it is a json with a html header
        """
        for num,i in enumerate(attributes):
            temp = i.split(" ")
            #needed because space bars in html has to be encoded with %20
            api += "%20".join(temp) + "&"
        request = f"GET {api} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        connection = HttpRequest.establish_Connection(host)
        secure_con = HttpRequest.ssl_wrapper(host, connection)
        
        secure_con.sendall(request.encode())
        response = b""
        while True:
            chunk = secure_con.recv(4096) #industry standard for size of chunks to communicate with
            if not chunk:
                break
            response += chunk
        
        response_text = response.decode()
        code, text = HttpRequest.status_code(response_text)
        code = int(code)
        if code != 200:
            raise HttpException.exception(code, text, host)
            
        secure_con.close()
        return response_text

class JsonHandling:
    def extractingJson(data: str) -> json:
        """Extracting json part of the Http get request, disregarding header"""
        parts = data.split("\r\n\r\n", 1)
        json_part = parts[1].strip()
        json_response = json.loads(json_part)
        return json_response
    
    def pretty_json(ugly_json: json) -> json:
        return print(json.dumps(ugly_json, indent=4))
        


    