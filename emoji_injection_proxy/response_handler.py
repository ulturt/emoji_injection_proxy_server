import abc
import json
from collections import deque

from bs4 import BeautifulSoup, Tag
from proxy.http.parser import HttpParser

from emoji_injection_proxy.string_emojizer import emojize_string


class ResponseHandler(abc.ABC):
    def __init__(self, response: HttpParser):
        self.response = response

    @abc.abstractmethod
    def insert_emoji_to_response_data(self):
        pass


class HtmlResponseHandler(ResponseHandler):
    def insert_emoji_to_response_data(self) -> None:
        # todo: extract charset
        parsed_body = BeautifulSoup(self.response.body, from_encoding='utf-8', features="html.parser")
        for child in parsed_body.descendants:
            if isinstance(child, Tag) and child.string is not None:
                child.string = emojize_string(child.string)
        self.response.body = parsed_body.encode('utf-8')


class JsonResponseHandler(ResponseHandler):
    def insert_emoji_to_response_data(self):
        parsed_json = json.loads(self.response.body.decode('utf-8'))
        if not parsed_json:
            return
        dicts_queue = deque()
        dicts_queue.append(parsed_json)
        while dicts_queue:
            dict_part = dicts_queue.popleft()
            for key, value in dict_part.items():
                if isinstance(value, dict):
                    dicts_queue.append(value)
                if isinstance(value, str):
                    dict_part[key] = emojize_string(value)
        self.response.body = json.dumps(
            parsed_json,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
