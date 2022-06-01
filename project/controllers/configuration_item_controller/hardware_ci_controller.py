from project.controllers.base_controller import BaseController
from project.models.configuration_item.hardware_configuration_item import HardwareConfigurationItem
from project import db
from project.models.exceptions import ObjectNotFoundException


class HardwareConfigurationItemController(BaseController):
    object_class = HardwareConfigurationItem
    null_object_class = None

    @staticmethod
    def _verify_relations(hardware_configuration_item: HardwareConfigurationItem) -> None:
        """
        Must be implemented.
        """
        pass

    @classmethod
    def create(cls, **kwargs) -> HardwareConfigurationItem:
        """
        Creates and saves HardwareConfigurationItem object.
        """
        # cls._verify_relations(hardware_configuration_item)
        ci_item = HardwareConfigurationItem(**kwargs)
        db.session.add(ci_item)
        db.session.commit()
        return ci_item

    @classmethod
    def update(cls, item_id: int, **kwargs) -> HardwareConfigurationItem:
        """
        Updates and saves HardwareConfigurationItem object.
        """
        item = cls.load_by_id(item_id)
        if not item:
            raise ObjectNotFoundException(object_name="Hardware Configuration Item", object_id=item_id)
        # cls._verify_relations(item_id)
        item.update(**kwargs)
        db.session.commit()
        return item

    @classmethod
    def load_by_name(cls, item_name: str) -> HardwareConfigurationItem:
        """
        Updates and saves HardwareConfigurationItem object.
        """
        return cls.object_class.query.filter_by(name=item_name).first()

    
    
        