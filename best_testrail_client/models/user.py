from dataclasses import dataclass

from best_testrail_client.custom_types import ModelID
from best_testrail_client.models.basemodel import BaseModel


@dataclass
class User(BaseModel):
    email: str
    id: ModelID  # noqa: A003, VNE003
    is_active: bool
    name: str
