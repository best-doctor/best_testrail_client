from dataclasses import dataclass

from best_testrail_client.models.basemodel import BaseModel


@dataclass
class Template(BaseModel):
    id: int  # noqa: A003, VNE003
    is_default: bool
    name: str
