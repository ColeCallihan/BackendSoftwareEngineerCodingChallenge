from utils.RESTEnum import RESTEnum
import requests

def execute_api_call(url: str, request_type: RESTEnum, headers: dict = None, payload: dict = None) -> requests.Response:
    match request_type:
        case RESTEnum.GET:
            return requests.get(url, headers=headers, json=payload)
        case RESTEnum.POST:
            return requests.post(url, headers=headers, json=payload)
        case RESTEnum.DELETE:
            return requests.delete(url, headers=headers, json=payload)