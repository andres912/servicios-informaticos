from project.controllers.base_controller import BaseController
from project.models.configuration_item.software_configuration_item import SoftwareConfigurationItem
from project import db


class SoftwareConfigurationItemController(BaseController):
    object_class = SoftwareConfigurationItem
    null_object_class = None

    @staticmethod
    def _verify_relations(software_configuration_item: SoftwareConfigurationItem) -> None:
        """
        Must be implemented.
        """
        pass

    @classmethod
    def create(cls, **kwargs) -> SoftwareConfigurationItem:
        """
        Creates and saves SoftwareConfigurationItem object.
        """
        # cls._verify_relations(software_configuration_item)
        software_configuration_item = SoftwareConfigurationItem(**kwargs)
        db.session.add(software_configuration_item)
        db.session.commit()
        return software_configuration_item

    @classmethod
    def update(cls, item_id: int, **kwargs) -> SoftwareConfigurationItem:
        """
        Updates and saves SoftwareConfigurationItem object.
        """
        item = cls.load_by_id(item_id)
        # cls._verify_relations(item_id)
        item.update(**kwargs)
        db.session.commit()
        return item


    
    