from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from jinja2 import Template

import markdown
import os
import re

from markify.plugins import pluginsAdapter
adapterList=[
    pluginsAdapter.parameterAdapter,
    pluginsAdapter.requestAdapter,
]

def page_from_path(path_info):
    root_path = "{}/page/".format(str(settings.BASE_DIR))
    absolute_path = os.path.abspath(root_path + path_info)
    if absolute_path.startswith(root_path) == False:
        return "{}/main.md".format(root_path)
    file_path = "{}.md".format(absolute_path)
    if os.path.exists(file_path) == False:
        return "{}/404.md".format(root_path)
    return file_path

def create_property(request, path_info):
    settings_dict = {
        setting: str(getattr(settings, setting))
        for setting in dir(settings)
        if setting.isupper()
    }

    request_data = {
        'method': request.method,
        'path': request.path,
        'path_info': path_info
    }

    data = {
        "request": request_data,
        "settings":settings_dict,
        "property" :{
            "page_path" : page_from_path(path_info=path_info)
        }
    }
    return data

def extract_shebang(content):
    lines = content.splitlines(True)
    shebang_lines = []
    updated_lines = []

    for line in lines:
        if line.startswith('#!'):
            shebang_lines.append(line)
        else:
            updated_lines.append(line)

    updated_content = ''.join(updated_lines)
    return shebang_lines, updated_content

def execute_class_by_shebang(shebang_parts, data):
    method_name = "Run"
    tag_name = "tag"

    for cls in adapterList:
        if hasattr(cls, tag_name) and getattr(cls, tag_name) != shebang_parts[0]:
            continue
        if hasattr(cls, method_name) and callable(getattr(cls, method_name)):
            data = getattr(cls, method_name)(data=data, args=shebang_parts)
    return data

def execute_shebang(shebang_lines):
    if len(shebang_lines) < 1:
        return []
    ret = {}
    for shebang in shebang_lines:
        shebang_line = shebang.removeprefix("#!")
        shebang_line = re.sub(r'\s+', ' ', shebang_line)
        shebang_parts = shebang_line.split(' ', 1)
        ret = execute_class_by_shebang(shebang_parts=shebang_parts, data=ret)
    return ret

def execute_markdown_path(path_info):
    file_path = page_from_path(path_info=path_info)

    # read markdown file
    file = open(file_path, "r")
    content = file.read()
    file.close()

    # extract markdown shebang
    shebang, content = extract_shebang(content=content)
    json_data = execute_shebang(shebang_lines=shebang)
    return json_data, content

def render_page(request, path_info):
    property = create_property(request=request, path_info=path_info)
    json_data, content = execute_markdown_path(path_info=path_info)

    template = Template(content)
    return HttpResponse(markdown.markdown(template.render(__property=property, __data = json_data)))

def render_json(request, path_info):
    property = create_property(request=request, path_info=path_info)
    json_data, content = execute_markdown_path(path_info=path_info)
    
    return JsonResponse({
        "__property":property,
        "__data": json_data
    })