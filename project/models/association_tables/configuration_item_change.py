from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from project.models.base_model import BaseModel

HardwareConfigurationItemChange = Table(
    "hardware_ci_item_change",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True),
    Column("hardware_ci_item_id", Integer, ForeignKey("ci_hardware.id")),
    Column("change_id", Integer, ForeignKey("change.id")),
)

SoftwareConfigurationItemChange = Table(
    "software_ci_item_change",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True),
    Column("software_ci_item_id", Integer, ForeignKey("ci_software.id")),
    Column("change_id", Integer, ForeignKey("change.id")),
)

SLAConfigurationItemChange = Table(
    "sla_ci_item_change",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True),
    Column("sla_ci_item_id", Integer, ForeignKey("ci_sla.id")),
    Column("change_id", Integer, ForeignKey("change.id")),
)
