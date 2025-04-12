import requests
from grok_unoffical_api._headers_manager import HeadersManager
from grok_unoffical_api.grok_payload import GrokPayload
from grok_unoffical_api.grok_cookies import GrokCookies
from grok_unoffical_api.grok_response import parse_multi_json


class GrokClient:
    def __init__(self,headers_manager: HeadersManager = HeadersManager(),cookies: GrokCookies = None):
        self.headers = headers_manager.get_headers()
        self.cookies = cookies.to_dict()

    def new(self,messages : GrokPayload = None):
        response = requests.post(
            "https://grok.com/rest/app-chat/conversations/new",
            headers=self.headers,
            cookies=self.cookies,
            json=messages.__dict__
        )
        if response.status_code == 200:
            return parse_multi_json(response.text)
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")


    def responses(self,conversation_id:str,data : GrokPayload = None):
        response = requests.post(
            f"https://grok.com/rest/app-chat/conversations/{conversation_id}/responses",
            headers=self.headers,
            cookies=self.cookies,
            json= data.__dict__
        )
        if response.status_code == 200:
            return parse_multi_json(response.text)
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")



