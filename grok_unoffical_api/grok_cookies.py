from dataclasses import dataclass


@dataclass
class GrokCookies:
    x_anonuserid: str
    x_challenge: str
    x_signature: str
    sso_rw: str
    sso:str

    def to_dict(self) -> dict:
        return {
            "x-anonuserid": self.x_anonuserid,
            "x-challenge": self.x_challenge,
            "x-signature": self.x_signature,
            "sso-rw": self.sso_rw,
            "sso": self.sso
        }



