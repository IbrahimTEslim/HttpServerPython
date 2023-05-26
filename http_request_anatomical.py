class HttpAnatomical():
    def __init__(self, request) -> None:
        self.__headers = {}
        self.__query_param = None
        self.__body = {}
        self.__dissect_request(request)
    
    def __dissect_request(self, request):
        headers, *body = request.split("\r\n\r\n")
        headers = headers.split("\r\n")
        self.__fetch_query_param(headers[0])

    
    def get_query_param(self):
        return self.__query_param
    
    def __fetch_query_param(self, http_head):
        parts = http_head.split(' ')
        self.__query_param = parts[1][1:]
    
    def get_headers(self):
        return self.__headers
    
    def get_body(self):
        return self.__body
