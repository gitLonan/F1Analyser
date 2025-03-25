#My classes
from src.network.http import HttpRequest
from src.network.errors.httpexception import HttpException
from src.DataExtraction.jsonhandling import JsonHandling

#My func
from urllib.parse import quote


from enum import Enum
import json

class API(Enum):
    DRIVERS = "/v1/drivers?"
    LAPS = "/v1/laps?"
    POSITION = "/v1/position?"
    STINTS = "/v1/stints?"
    SESSIONS = "/v1/sessions?"
    MEETINGS = "/v1/meetings?"

class ApiCommunication:

    def communication(host: str, api: str =None,attributes: list[str]=[]) -> json:
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

    def get_api(host: str, api_path: str, attr: list[str] =[]) -> json:
        """
            Args:
                host (str) - link to the server(or rather DSN name) 
                api_path (str) - path to the api(on the server ofc)
                attr (list[str]) - list by which a persone can specify the data    
        """
        data_drivers = ApiCommunication.communication(host, api_path, attributes=attr)
        json_part = JsonHandling.extracting_json(data_drivers)
        return json_part
    

    




        


    