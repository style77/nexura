from dataclasses import dataclass
from typing import Dict


@dataclass
class Response:
    type: str
    content: str


@dataclass
class Example:
    label: str
    code: Dict[str, str]
    response: Response
