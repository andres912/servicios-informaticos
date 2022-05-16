from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from project.models.base_model import BaseModel

HardwareConfigurationItemIncident = Table(
    "hardware_ci_item_incident",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True),
    Column("hardware_ci_item_id", Integer, ForeignKey("ci_hardware.id")),
    Column("incident_id", Integer, ForeignKey("incident.id")),
)

SoftwareConfigurationItemIncident = Table(
    "software_ci_item_incident",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True),
    Column("software_ci_item_id", Integer, ForeignKey("ci_software.id")),
    Column("incident_id", Integer, ForeignKey("incident.id")),
)

SLAConfigurationItemIncident = Table(
    "sla_ci_item_incident",
    BaseModel.metadata,
    Column("id", Integer, primary_key=True),
    Column("sla_ci_item_id", Integer, ForeignKey("ci_sla.id")),
    Column("incident_id", Integer, ForeignKey("incident.id")),
)
