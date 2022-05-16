
from datetime import datetime
from project.models.configuration_item.configuration_item import ConfigurationItem
from project import db
from project.models.priority import PRIORITY_MEDIUM
from project.models.association_tables.configuration_item_incident import HardwareConfigurationItemIncident


class HardwareConfigurationItem(ConfigurationItem):
    __tablename__ = "ci_hardware"

    type = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(200), nullable=False)
    serial_number = db.Column(db.String(100), nullable=False)
    price = db.Column(db.BigInteger, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    incidents = db.relationship("Incident", secondary="hardware_ci_item_incident")

    def __init__(
        self,
        type: str = None,
        manufacturer: str = None,
        serial_number: str = None,
        price: float = None,
        purchase_date: datetime = None,
        **kwargs
    ):
        super().__init__(item_class="Hardware", **kwargs)
        self.type = type
        self.manufacturer = manufacturer
        self.serial_number = serial_number
        self.price = price
        self.purchase_date = purchase_date

    def _update(
        self,
        type: str = None,
        manufacturer: str = None,
        serial_number: str = None,
        price: float = None,
        purchase_date: datetime = None,
        **kwargs
    ) -> None:
        super()._update(**kwargs)
        if type:
            self.type = type
        if manufacturer:
            self.manufacturer = manufacturer
        if serial_number:
            self.serial_number = serial_number
        if price:
            self.price = price
        if purchase_date:
            self.purchase_date = purchase_date

        
