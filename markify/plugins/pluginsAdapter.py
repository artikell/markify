import requests
from urllib.parse import urlparse, parse_qs, parse_qsl
from jsonpath_ng import parse

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
        parsed_query = parse_qs(params_str)
        for key, value in parsed_query.items():
            parsed_query[key] = value[0]

        response = requests.get(url, params=parsed_query)
        response_dict = []

        if response.status_code == 200:
            response_dict = response.json()
        else:
            print("请求失败，状态码:", response.status_code)

        return response_dict