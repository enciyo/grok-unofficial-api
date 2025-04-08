# Grok Unofficial API

This is an unofficial Python API for Grok.

## Installation

First, clone the repository:

```bash
git clone <repository_url>
cd grok_unoffical_api
pip install .
```

Then, install the package:

```bash
pip install grok-unoffical-api==0.1.0
```

## Usage

```python
import os
from grok_client import GrokClient
from grok_payload import GrokPayload
from grok_cookies import GrokCookies

if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

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
```

## Files

*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
*   `MANIFEST.in`: Specifies files to include in the distribution.
*   `pyproject.toml`: Specifies the build system requirements.
*   `requirements.txt`: Specifies the project's dependencies.
*   `setup.py`: Specifies the project's metadata and dependencies.
*   `grok_unoffical_api/__init__.py`: Initializes the `grok_unoffical_api` package.
*   `grok_unoffical_api/_example.py`: An example of how to use the API.
*   `grok_unoffical_api/_headers_manager.py`: Manages the headers for the API requests.
*   `grok_unoffical_api/grok_client.py`: The main API client.
*   `grok_unoffical_api/grok_cookies.py`: Defines the `GrokCookies` class.
*   `grok_unoffical_api/grok_payload.py`: Defines the `GrokPayload` class.
*   `grok_unoffical_api/grok_response.py`: Parses the API responses.
