from dataclasses import dataclass

from best_testrail_client.models.basemodel import BaseModel


@dataclass
class Status(BaseModel):
    color_bright: int
    color_dark: int
    color_medium: int
    id: int  # noqa: A003, VNE003
    is_final: bool
    is_system: bool
    is_untested: bool
    label: str
    name: str
