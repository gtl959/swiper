from django.http import JsonResponse

from common import errors


def render_json(code=errors.OK,data=None):
    result = {
        'code':code,
    }

    if data:
        result['data'] = data

    json_dumps_params = {
        'separators':(',',':')
    }

    return JsonResponse(data=result,json_dumps_params=json_dumps_params)
