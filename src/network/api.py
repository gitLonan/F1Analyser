from src.network.http import HttpRequest
from urllib.parse import quote
from enum import Enum
import json

class API(Enum):
    DRIVERS = "/v1/drivers?"
    LAPS = "/v1/laps?"

class ApiCommunication():

    def get_api(host, api=None,attributes=[]) -> json:
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
            chunk = secure_con.recv(4096)
            if not chunk:
                break
            response += chunk
        response_text = response.decode()
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsss", response_text)
        secure_con.close()
        return response_text

    def extractingJson(data) -> json:
        parts = data.split("\r\n\r\n", 1)
        json_part = parts[1].strip()
        json_response = json.loads(json_part)
        return json_response
    
    def pretty_json(ugly_json):
        return print(json.dumps(ugly_json, indent=4))


    