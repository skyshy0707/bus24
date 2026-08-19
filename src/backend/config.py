from dataclasses import dataclass
import os

@dataclass
class config:
    SECRET_AUTH_KEY: str = os.getenv("SECRET_AUTH_KEY")
