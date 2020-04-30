from dataclasses import dataclass
from typing import Optional

from best_testrail_client.custom_types import ModelID
from best_testrail_client.models.basemodel import BaseModel


@dataclass
class Section(BaseModel):
    name: str
    depth: Optional[int] = None
    description: Optional[str] = None
    display_order: Optional[int] = None
    id: Optional[ModelID] = None  # noqa: A003, VNE003
    parent_id: Optional[ModelID] = None
    suite_id: Optional[ModelID] = None
