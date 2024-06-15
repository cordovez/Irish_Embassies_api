import pydantic
from pydantic import Field

from models.embassy import EmbassyModel
from models.consulate import ConsulateModel
from models.representation import RepresentationModel


class MissionModel(pydantic.BaseModel):
    mission: EmbassyModel | ConsulateModel | RepresentationModel = Field(
        discriminator="type_of"
    )
