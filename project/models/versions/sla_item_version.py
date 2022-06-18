from datetime import datetime
from project import db
from project.models.versions.item_version import ItemVersion


class SLAItemVersion(ItemVersion):
    __tablename__ = "item_sla_version"

    service_type = db.Column(db.String(100), nullable=False)
    service_manager = db.Column(db.String(100), nullable=False)
    client = db.Column(db.String(200), nullable=False)
    starting_date = db.Column(db.DateTime, nullable=False)
    ending_date = db.Column(db.DateTime, nullable=False)
    measurement_unit = db.Column(db.String(100), nullable=False)
    measurement_value = db.Column(db.Integer, nullable=False)
    is_crucial = db.Column(db.Boolean, default=False, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("ci_sla.id"), nullable=False)

    def __init__(
        self,
        service_type: str = None,
        service_manager: str = None,
        client: str = None,
        starting_date: datetime = None,
        ending_date: datetime = None,
        measurement_unit: str = None,
        measurement_value: int = None,
        is_crucial: bool = False,
        **kwargs
    ):

        super().__init__(**kwargs)
        self.service_type = service_type
        self.service_manager = service_manager
        self.client = client
        self.starting_date = starting_date
        self.ending_date = ending_date
        self.measurement_unit = measurement_unit
        self.measurement_value = measurement_value
        self.is_crucial = is_crucial

    def _update(
        self,
        service_type: str = None,
        service_manager: str = None,
        client: str = None,
        starting_date: datetime = None,
        ending_date: datetime = None,
        measurement_unit: str = None,
        measurement_value: int = None,
        is_crucial: bool = False,
        **kwargs
    ) -> None:
        super()._update(**kwargs)
        if service_type:
            self.service_type = service_type
        if service_manager:
            self.service_manager = service_manager
        if client:
            self.client = client
        if starting_date:
            self.starting_date = starting_date
        if ending_date:
            self.ending_date = ending_date
        if measurement_unit:
            self.measurement_unit = measurement_unit
        if measurement_value:
            self.measurement_value = measurement_value
        if is_crucial is not None: # has to be different, because it is a boolean
            self.is_crucial = is_crucial

            
