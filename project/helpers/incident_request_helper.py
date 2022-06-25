from project.controllers.configuration_item_controller.hardware_ci_controller import (
    HardwareConfigurationItemController,
)
from project.controllers.configuration_item_controller.sla_ci_controller import (
    SLAConfigurationItemController,
)
from project.controllers.configuration_item_controller.software_ci_controller import (
    SoftwareConfigurationItemController,
)
from project.models.exceptions import ObjectNotFoundException


class IncidentRequestHelper:
    @classmethod
    def get_configuration_item_id(
        cls, item_name, hardware_list, software_list, sla_list
    ):
        try: #try hardware
            hardware_ci_item = HardwareConfigurationItemController.load_by_name(item_name)
            if hardware_ci_item:
                hardware_list.append(hardware_ci_item)
                return
        except ObjectNotFoundException:
            try: #no success, try software
                software_ci_item = SoftwareConfigurationItemController.load_by_name(item_name)
                if software_ci_item:
                    software_list.append(software_ci_item)
                    return
            except ObjectNotFoundException: #last try
                    sla_ci_item = SLAConfigurationItemController.load_by_name(item_name)
                    if sla_ci_item:
                        sla_list.append(sla_ci_item)
                        return

    @classmethod
    def get_configuration_items(cls, item_names):
        """
        Get all configuration items by name
        """
        hardware_list = []
        software_list = []
        sla_list = []
        for item_name in item_names:
            cls.get_configuration_item_id(
                item_name, hardware_list, software_list, sla_list
            )
        return hardware_list, software_list, sla_list

    @classmethod
    def create_incident_request(cls, raw_request):
        request = {}
        request["description"] = raw_request["description"]
        request["priority"] = raw_request["priority"]
        request["created_by"] = raw_request["created_by"]
        item_names = [raw_request[item] for item in raw_request if item.startswith("item_name")]
        hardware_cis, software_cis, sla_cis = cls.get_configuration_items(item_names)
        request["hardware_configuration_items"] = hardware_cis
        request["software_configuration_items"] = software_cis
        request["sla_configuration_items"] = sla_cis
        return request

