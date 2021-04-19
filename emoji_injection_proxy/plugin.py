from typing import Any, Optional

from proxy.common.utils import bytes_
from proxy.http.parser import HttpParser, httpParserStates, httpParserTypes
from proxy.http.proxy import HttpProxyBasePlugin

from emoji_injection_proxy.response_handler import HtmlResponseHandler, JsonResponseHandler


class EmojiInjectionPlugin(HttpProxyBasePlugin):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.response = HttpParser(httpParserTypes.RESPONSE_PARSER)

    def before_upstream_connection(self, request: HttpParser) -> Optional[HttpParser]:
        return request

    def handle_client_request(self, request: HttpParser) -> Optional[HttpParser]:
        return request

    def handle_upstream_chunk(self, chunk: memoryview) -> memoryview:
        self.response.parse(chunk.tobytes())
        if self.response.state == httpParserStates.COMPLETE:
            self.handle_response_data()
            new_content_length = len(self.response.body)
            bytes_header_name = b'content-length'
            self.response.add_header(bytes_header_name, bytes_(new_content_length))
            self.client.queue(memoryview(self.response.build_response()))
        return memoryview(b'')

    def on_upstream_connection_close(self) -> None:
        pass

    def handle_response_data(self) -> None:
        if 'text/html' in self.response.header(b'content-type').decode():
            response_handler = HtmlResponseHandler(self.response)
        elif 'application/json' == self.response.header(b'content-type').decode():
            response_handler = JsonResponseHandler(self.response)
        else:
            return
        response_handler.insert_emoji_to_response_data()
