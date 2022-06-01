from project.controllers.base_controller import BaseController
from project.models.configuration_item.sla_configuration_item import SLAConfigurationItem
from project import db


class SLAConfigurationItemController(BaseController):
    object_class = SLAConfigurationItem
    null_object_class = None

    @staticmethod
    def _verify_relations(sla_configuration_item: SLAConfigurationItem) -> None:
        """
        Must be implemented.
        """
        pass

    @classmethod
    def create(cls, **kwargs) -> SLAConfigurationItem:
        """
        Creates and saves SLAConfigurationItem object.
        """
        # cls._verify_relations(sla_configuration_item)
        sla_configuration_item = SLAConfigurationItem(**kwargs)
        db.session.add(sla_configuration_item)
        db.session.commit()
        return sla_configuration_item

    @classmethod
    def update(cls, item_id: int, **kwargs) -> SLAConfigurationItem:
        """
        Updates and saves SLAConfigurationItem object.
        """
        item = cls.load_by_id(item_id)
        # cls._verify_relations(item_id)
        item.update(**kwargs)
        db.session.commit()
        return item


    @classmethod
    def load_by_name(cls, item_name: str) -> SLAConfigurationItem:
        """
        Updates and saves HardwareConfigurationItem object.
        """
        return cls.object_class.query.filter_by(name=item_name).first()

    