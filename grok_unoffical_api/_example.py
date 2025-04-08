
import os
from grok_client import GrokClient
from grok_payload import GrokPayload
from grok_cookies import GrokCookies

if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()



if __name__ == "__main__":


    grok_client = GrokClient(
        cookies=GrokCookies(
            x_challenge=os.getenv("X_CHALLENGE"),
            x_anonuserid=os.getenv("X_ANONUSERID"),
            x_signature=os.getenv("X_SIGNATURE"),
            sso=os.getenv("SSO"),
            sso_rw=os.getenv("SSO_RW")
        )
    )
    new = grok_client.new(GrokPayload(message="My name is Enciyo."))

    for r in new:
        if r.response and r.response.modelResponse:
            print(r.response.modelResponse.message)
        if r.conversation and r.conversation.conversationId:
            conversation_id = r.conversation.conversationId

    responses = grok_client.responses(
        conversation_id=conversation_id,
        data=GrokPayload(message="What's my name?"),
    )

    for r in responses:
        if r.response and r.response.modelResponse:
            print(r.response.modelResponse.message)
