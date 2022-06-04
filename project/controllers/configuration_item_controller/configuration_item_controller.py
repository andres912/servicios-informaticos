from project.controllers.base_controller import BaseController
from project.models.configuration_item.configuration_item import ConfigurationItem
from project import db
from project.models.exceptions import InvalidItemVersionsException, ObjectNotFoundException


class ConfigurationItemController(BaseController):
    object_class = ConfigurationItem
    null_object_class = None

    @staticmethod
    def _verify_relations(hardware_configuration_item: ConfigurationItem) -> None:
        """
        Must be implemented.
        """
        pass

    @classmethod
    def verify_versions(cls, item_version: int, item_family_id: int) -> None:
        """
        Verifies that the item family and item version exist.
        """
        if item_version == 1 and item_family_id != None:
            raise InvalidItemVersionsException(item_version=item_version, item_family_id=item_family_id)
        if item_version != 1 and item_family_id == None:
            raise InvalidItemVersionsException(item_version=item_version)


    @classmethod
    def update_versions(cls, item_version, item_family_id):
        """
        Updates the item's first version if this version is the second one
        """
        if item_version != 2: # solamente tiene que actualizar en la versión 2
            return

        first_version_item = cls.object_class.query.filter_by(id=item_family_id).first()
        if not first_version_item:
            raise ObjectNotFoundException(object_name="Configuration Item", object_id=item_family_id)
        
        first_version_item.item_family_id = item_family_id
        db.session.commit()

    @classmethod
    def create(cls, **kwargs) -> ConfigurationItem:
        """
        Creates and saves HardwareConfigurationItem object.
        """
        item_version = kwargs.get("version", 1)
        item_family_id = kwargs.get("item_family_id", None)

        cls.verify_versions(item_version, item_family_id)
        ci_item = cls.object_class(**kwargs)
        db.session.add(ci_item)
        db.session.commit()

        cls.update_versions(item_version, item_family_id)
        return ci_item

    @classmethod
    def update(cls, item_id: int, **kwargs) -> ConfigurationItem:
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
    def load_by_name(cls, item_name: str) -> ConfigurationItem:
        """
        Updates and saves HardwareConfigurationItem object.
        """
        return cls.object_class.query.filter_by(name=item_name).first()

    
    
        