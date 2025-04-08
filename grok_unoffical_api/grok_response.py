from dataclasses import dataclass

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import re


def parse_datetime(dt_str: str) -> datetime:
    match = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\.(\d+)Z", dt_str)
    if match:
        base_time_str = match.group(1)
        microseconds_str = match.group(2)

        microseconds = int(microseconds_str)
        microseconds = round(microseconds / (10 ** (len(microseconds_str) - 6)))

        datetime_obj = datetime.strptime(base_time_str, "%Y-%m-%dT%H:%M:%S")
        datetime_obj = datetime_obj.replace(microsecond=microseconds)
        return datetime_obj
    else:
        raise ValueError(f"Geçersiz tarih formatı: {dt_str}")

@dataclass
class BaseResponse:
    responseId: str
    message: str
    sender: str
    createTime: datetime
    manual: bool
    partial: bool
    shared: bool
    query: str
    queryType: str
    webSearchResults: List[str]
    xpostIds: List[str]
    xposts: List[str]
    generatedImageUrls: List[str]
    imageAttachments: List[str]
    fileAttachments: List[str]
    cardAttachmentsJson: List[str]
    fileUris: List[str]
    fileAttachmentsMetadata: List[str]
    isControl: bool
    steps: List[str]
    imageEditUris: List[str]
    mediaTypes: List[str]
    webpageUrls: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseResponse':
        return cls(
            responseId=data["responseId"],
            message=data["message"],
            sender=data["sender"],
            createTime=parse_datetime(data["createTime"]),
            manual=data["manual"],
            partial=data["partial"],
            shared=data["shared"],
            query=data["query"],
            queryType=data["queryType"],
            webSearchResults=data["webSearchResults"],
            xpostIds=data["xpostIds"],
            xposts=data["xposts"],
            generatedImageUrls=data["generatedImageUrls"],
            imageAttachments=data["imageAttachments"],
            fileAttachments=data["fileAttachments"],
            cardAttachmentsJson=data["cardAttachmentsJson"],
            fileUris=data["fileUris"],
            fileAttachmentsMetadata=data["fileAttachmentsMetadata"],
            isControl=data["isControl"],
            steps=data["steps"],
            imageEditUris=data["imageEditUris"],
            mediaTypes=data["mediaTypes"],
            webpageUrls=data["webpageUrls"]
        )

@dataclass
class UserResponse(BaseResponse):
    pass

@dataclass
class ModelResponse(BaseResponse):
    parentResponseId: str
    metadata: Dict[str, str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelResponse':
        base = BaseResponse.from_dict(data)
        return cls(
            **vars(base),
            parentResponseId=data["parentResponseId"],
            metadata=data["metadata"]
        )

@dataclass
class Conversation:
    conversationId: str
    title: str
    starred: bool
    createTime: datetime
    modifyTime: datetime
    systemPromptName: str
    temporary: bool
    mediaTypes: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        return cls(
            conversationId=data["conversationId"],
            title=data["title"],
            starred=data["starred"],
            createTime=parse_datetime(data["createTime"]),
            modifyTime=parse_datetime(data["modifyTime"]),
            systemPromptName=data["systemPromptName"],
            temporary=data["temporary"],
            mediaTypes=data["mediaTypes"]
        )

@dataclass
class TokenResponse:
    token: str
    isThinking: bool
    isSoftStop: bool
    responseId: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TokenResponse':
        return cls(
            token=data["token"],
            isThinking=data["isThinking"],
            isSoftStop=data["isSoftStop"],
            responseId=data["responseId"]
        )

@dataclass
class Response:
    userResponse: Optional[UserResponse] = None
    modelResponse: Optional[ModelResponse] = None
    token: Optional[TokenResponse] = None
    isThinking: bool = False
    isSoftStop: bool = False
    responseId: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Response':
        user_response = UserResponse.from_dict(data["userResponse"]) if "userResponse" in data else None
        model_response = ModelResponse.from_dict(data["modelResponse"]) if "modelResponse" in data else None
        token = TokenResponse.from_dict(data) if "token" in data else None
        return cls(
            userResponse=user_response,
            modelResponse=model_response,
            token=token,
            isThinking=data.get("isThinking", False),
            isSoftStop=data.get("isSoftStop", False),
            responseId=data.get("responseId", "")
        )


@dataclass
class ConversationResult:
    conversation: Optional[Conversation] = None
    response: Optional[Response] = None
    title: Optional[Dict[str, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationResult':
        result = data.get("result", {})
        if "conversation" in result:
            return cls(conversation=Conversation.from_dict(result["conversation"]))
        elif "response" in result:
            return cls(response=Response.from_dict(result["response"]))
        elif "title" in result:
            return cls(title=result["title"])
        elif "modelResponse" in result:
            return cls(response= Response(
                modelResponse=ModelResponse.from_dict(result["modelResponse"]),
            ))
        return cls()

def parse_multi_json(text: str) -> List[ConversationResult]:
    json_objects = re.findall(r'\{.*?\}(?=\s*\{|$)', text, re.DOTALL)
    results = []

    for json_str in json_objects:
        try:
            data = json.loads(json_str.strip())
            result = ConversationResult.from_dict(data)
            results.append(result)
        except json.JSONDecodeError as e:
            print(f"JSON ayrıştırma hatası: {e} - Geçersiz JSON: {json_str}")

    return results
