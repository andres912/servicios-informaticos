
from datetime import datetime
from project.models.versions.item_version import ItemVersion
from project import db


class HardwareItemVersion(ItemVersion):
    __tablename__ = "item_hardware_version"

    type = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(200), nullable=False)
    serial_number = db.Column(db.String(100), nullable=False)
    price = db.Column(db.BigInteger, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("ci_hardware.id"), nullable=False)
    change = db.relationship("Change")

    def __init__(
        self,
        type: str = None,
        manufacturer: str = None,
        serial_number: str = None,
        price: float = None,
        purchase_date: datetime = None,
        **kwargs
    ):
        super().__init__(**kwargs)
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

        
