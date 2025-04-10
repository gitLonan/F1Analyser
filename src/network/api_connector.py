import socket

#My classes
from src.network.http_requester import HttpRequest
from src.network.errors.httpexception import HttpException
from src.data_extraction.jsonhandling import JsonHandling

#My func
from urllib.parse import quote


from enum import Enum
import json
import sys

class API(Enum):
    DRIVERS = "/v1/drivers?"
    LAPS = "/v1/laps?"
    POSITION = "/v1/position?"
    STINTS = "/v1/stints?"
    SESSIONS = "/v1/sessions?"
    MEETINGS = "/v1/meetings?"

class ApiCommunication:
    @staticmethod
    def communication(host: str, api: str =None, attributes: list[str]=[]) -> json:
        """ 
            Args:
                host (str) - websites domain name, example api.openf1.org
                api (str) - path to the resource on the hosts server
                attributes (list[str]) - found on the site https://openf1.org/

            Returns:
                response_text (json) - it is a json with a html header
        """
        for num,i in enumerate(attributes):
            print("OVO GELDM", i)
            #needed because space bars in html has to be encoded with %20
            api += i + "&"
        #try curl -v "url" - this to check if the request needs additional headers
        print(api)
        request = (
        f"GET {api} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"user-agent: curl/7.81.0\r\n"
        f"Accept: */*\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
        connection = HttpRequest.establish_Connection(host)
        secure_con = HttpRequest.ssl_wrapper(host, connection)
        
        secure_con.sendall(request.encode())
        response = b""
        while True:
            try:
                chunk = secure_con.recv(4096) #industry standard for size of chunks to communicate with
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                print("Socket timed out")
                break
        response_text = response.decode()
        print("Raw response`", response_text)
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

            Return:
                json part of the response
        """
        response_data = ApiCommunication.communication(host, api_path, attributes=attr)
        json_part = JsonHandling.extracting_json(response_data)
        if len(json_part) == 0:
            print("Entered invalid year or API path, can't go below 2023 and above 2025(for now) - date: 3.26.2025")
            sys.exit()

        return json_part
    

    




        


    