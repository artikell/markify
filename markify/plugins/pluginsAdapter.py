import requests


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
    tag = "request"
    @staticmethod
    def Run(data, args):
        if len(args) < 1:
            return data
        url = args[1]
        response = requests.get(url)
        response_dict = []
        # 检查响应状态码
        if response.status_code == 200:
            # 解析 JSON 响应为字典
            response_dict = response.json()
        else:
            print("请求失败，状态码:", response.status_code)
        return response_dict