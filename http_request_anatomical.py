"""
    This File has the functions to deal with HTTP requests, fetch the required information
    or do what is needed.
"""

import json

class HttpAnatomical():
    def __init__(self, request) -> None:
        self.__request = request
        self.__headers = {}
        self.__query_param = None
        self.__request_method = None
        self.__body = {}
        self.__dissect_request(request)
    
    def __dissect_request(self, request):
        headers, *body = request.split("\r\n\r\n")
        headers = headers.split("\r\n")
        self.__fetch_query_param(headers[0])
        # self.__jsonify_headers(headers[1:])
        # self.__josnify_body(body)
    
    def get_query_param(self):
        return self.__query_param
    
    def __jsonify_headers(self, headers_list):
        headers_str = "{"
        for h in headers_list: headers_str +=  "\"" + h.split(": ")[0] + "\":\"" + h.split(": ")[1] + "\"," 
        headers_str = headers_str[:-1] + "}"
        self.__headers = json.loads(headers_str)
    
    def __josnify_body(self, body):
        self.__body = json.loads(body)
    
    def __fetch_query_param(self, http_head):
        parts = http_head.split(' ')
        if len(parts) == 1: return
        self.__request_method = parts[0]
        self.__query_param = parts[1][1:]
    
    def get_headers(self):
        return self.__headers
    
    def get_body(self):
        return self.__body
    
        
        