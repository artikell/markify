import requests
from urllib.parse import urlparse, parse_qs, parse_qsl

class parameterAdapter:
    tag = "tag"
    @staticmethod
    def Run(data, args):
        if len(args) < 1:
            return data
        value = args[1]
        items = value.split("=", 1)
        if len(items) < 2:
            return data
        data[items[0]] = items[1]
        return data

class requestAdapter:
    tag = "GET-request"
    @staticmethod
    def Run(data, args):
        if len(args) < 2:
            return data

        url, params_str = args
        params = parse_qs(params_str)
        response = requests.get(url, params=params)
        response_dict = []

        if response.status_code == 200:
            response_dict = response.json()
        else:
            print("请求失败，状态码:", response.status_code)
        return response_dict