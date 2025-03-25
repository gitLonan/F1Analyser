import socket

class HttpException(Exception):

    @classmethod
    def exception(cls, code, text, host):
        if 400 <= code < 500:
            return ClientError.error(code, text, host)
        elif 500 <= code < 600:
             return ServerError.error(code, text, host)
    

class ClientError(HttpException):
    @classmethod
    def error(cls, code, text, host):
        message = f"""
            Error: {code} {text}
            Connecting to: {host}
            """
        return cls(message)

class ServerError(HttpException):
    @classmethod
    def error(cls, code, text, host):
        message = f"""
            Error: {code} {text}
            Connecting to: {host}

            Check if your api is correct, maybe there is some kind of typo
            """
        return cls(message)
    


