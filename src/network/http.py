import ssl
import socket



class HttpRequest():
    global port
    port = 443
    

    def establish_Connection(host):
        try:
            raw_socket = socket.create_connection((host, port), timeout=5)
            return raw_socket
        except Exception:
            print("Something is wrong")

    def ssl_wrapper(host, socket):
        secure = ssl.create_default_context().wrap_socket(socket, server_hostname=host)
        return secure
        


