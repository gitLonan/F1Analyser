import ssl
import socket
import sys


class HttpRequest():
    global port
    port = 443

    def establish_Connection(host):
        try:
            raw_socket = socket.create_connection((host, port), timeout=5)
            return raw_socket
        except socket.gaierror as error:
           print(f"Error: {error.errno}, Message: {error.strerror}")
           sys.exit()

    def ssl_wrapper(host, socket):
        """ Wraps socket with ssl for HTTPS """
        secure = ssl.create_default_context().wrap_socket(socket, server_hostname=host)
        return secure
    
    def status_code(response: str) -> tuple[str,str]:
        """ Extracts HTTP status code from the response """
        splited_response = response.split("\r\n")
        code = splited_response[0].split(" ")[1]
        text = splited_response[0].split(" ")[2]
        print(code, text)
        return code, text
        


