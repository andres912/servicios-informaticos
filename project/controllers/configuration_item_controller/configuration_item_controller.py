from typing import List

from sqlalchemy import text
from project.controllers.base_controller import BaseController
from project.models.configuration_item.configuration_item import ConfigurationItem
from project import db
from project.models.exceptions import (
    InvalidItemVersionsException,
    ItemVersionNotFoundException,
    ObjectNotFoundException,
)
from project.models.versions.item_version import ItemVersion


class ConfigurationItemController(BaseController):
    object_class = ConfigurationItem
    null_object_class = None
    object_version_class = ItemVersion

    @staticmethod
    def _verify_relations(hardware_configuration_item: ConfigurationItem) -> None:
        """
        Must be implemented.
        """
        pass

    @classmethod
    def create(cls, **kwargs) -> ConfigurationItem:
        """
        Creates and saves HardwareConfigurationItem object.
        """
        item = cls.object_class(**kwargs)
        db.session.add(item)
        db.session.commit()  # necesario para tener el id

        kwargs["item_id"] = item.id
        item_version = cls.object_version_class(**kwargs)
        db.session.add(item_version)
        db.session.commit()

        item.set_current_version(item_version.id)
        db.session.commit()

        return item

    @classmethod
    def update(cls, item_id: int, **kwargs) -> ConfigurationItem:
        """
        Updates and saves HardwareConfigurationItem object.
        """
        item = cls.load_by_id(item_id)
        if not item:
            raise ObjectNotFoundException(
                object_name="Hardware Configuration Item", object_id=item_id
            )
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

    @classmethod
    def restore_item_version(cls, item_id: int, item_version: int):
        item = cls.load_by_id(item_id)
        new_version = cls.object_version_class.query.filter_by(
            item_id=item_id, version=item_version
        ).first()
        if not new_version:
            raise ItemVersionNotFoundException(
                item_id=item_id, item_version=item_version
            )
        item.current_version_id = new_version.id
        db.session.commit()
        return item

    @classmethod
    def load_all(cls) -> List[ConfigurationItem]:
        """
        Returns all Model objects, filtered by not deleted.
        """
        return cls.object_class.query.filter_by(
            is_deleted=False
        ).all()

    @classmethod
    def create_new_item_version(cls, item_id: int, **kwargs):
        item = cls.load_by_id(item_id)
        new_version_number = item.last_version + 1

        kwargs["version_number"] = new_version_number
        kwargs["item_id"] = item_id
        
        new_version = cls.object_version_class(**kwargs)
        db.session.add(new_version)
        db.session.commit()

        item.last_version = new_version_number
        item.set_current_version(new_version.id)
        db.session.commit()

        return item

    @classmethod
    def create_draft(cls, item_id: int, change_id: int, **kwargs):
        item = cls.load_by_id(item_id)

        kwargs["item_id"] = item_id
        kwargs["is_draft"] = True
        kwargs["change_id"] = change_id
        del kwargs["draft_change_id"]
        
        new_version = cls.object_version_class(**kwargs)
        db.session.add(new_version)
        db.session.commit()

        item.set_draft(new_version.id)
        db.session.commit()

        return new_version


    @classmethod
    def load_by_name(cls, object_name: str) -> None:
        item_table_name = cls.object_class.__tablename__
        item_version_table_name = cls.object_version_class.__tablename__
        query = """
            SELECT {item_table_name}.id FROM {item_table_name} JOIN {version_table_name} ON {item_table_name}.current_version_id = {version_table_name}.id
            WHERE {version_table_name}.name = '{object_name}'
        """.format(
            item_table_name=item_table_name,
            version_table_name=item_version_table_name,
            object_name=object_name,
        )

        query = text(query)
        result = db.engine.execute(query)
        item = result.fetchone()
        if not item:
            raise ObjectNotFoundException(object_name="Item", object_id=object_name)
        id = item[0]
        return cls.load_by_id(id)