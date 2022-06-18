from project import db
from project.models.versions.item_version import ItemVersion


class SoftwareItemVersion(ItemVersion):
    __tablename__ = "item_software_version"

    provider = db.Column(db.String(200), nullable=False)
    software_version = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("ci_software.id"), nullable=False)

    def __init__(
        self,
        provider: str = None,
        software_version: str = None,
        type: str = None,
        **kwargs
    ):

        super().__init__(**kwargs)
        self.provider = provider
        self.software_version = software_version
        self.type = type

    def _update(
        self,
        provider: str = None,
        software_version: str = None,
        type: str = None,
        **kwargs
    ) -> None:
        super()._update(**kwargs)
        if provider:
            self.provider = provider
        if software_version:
            self.software_version = software_version
        if type:
            self.type = type









