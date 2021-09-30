from copy import copy
from typing import TYPE_CHECKING, Any, List, Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from ..payment.interface import (
    CustomerSource,
    GatewayResponse,
    PaymentData,
    PaymentGateway,
)
from .models import PluginConfiguration

if TYPE_CHECKING:
    # flake8: noqa
    from ..account.models import Address, User
    from ..order.models import Order
    from ..invoice.models import Invoice


PluginConfigurationType = List[dict]


class ConfigurationTypeField:
    STRING = "String"
    BOOLEAN = "Boolean"
    SECRET = "Secret"
    PASSWORD = "Password"
    CHOICES = [
        (STRING, "Field is a String"),
        (BOOLEAN, "Field is a Boolean"),
        (SECRET, "Field is a Secret"),
        (PASSWORD, "Field is a Password"),
    ]


class BasePlugin:
    """Abstract class for storing all methods available for any plugin.

    All methods take previous_value parameter.
    previous_value contains a value calculated by the previous plugin in the queue.
    If the plugin is first, it will use default value calculated by the manager.
    """

    PLUGIN_NAME = ""
    PLUGIN_ID = ""
    PLUGIN_DESCRIPTION = ""
    CONFIG_STRUCTURE = None
    DEFAULT_CONFIGURATION = []
    DEFAULT_ACTIVE = False

    def __init__(self, *, configuration: PluginConfigurationType, active: bool):
        self.configuration = self.get_plugin_configuration(configuration)
        self.active = active

    def __str__(self):
        return self.PLUGIN_NAME

    def webhook(self, request: WSGIRequest, path: str, previous_value) -> HttpResponse:
        """Handle received http request.

        Overwrite this method if the plugin expects the incoming requests.
        """
        return NotImplemented

    def change_user_address(
        self,
        address: "Address",
        address_type: Optional[str],
        user: Optional["User"],
        previous_value: "Address",
    ) -> "Address":
        return NotImplemented

    def order_created(self, order: "Order", previous_value: Any):
        """Trigger when order is created.

        Overwrite this method if you need to trigger specific logic after an order is
        created.
        """
        return NotImplemented

    def invoice_request(
        self,
        order: "Order",
        invoice: "Invoice",
        number: Optional[str],
        previous_value: Any,
    ) -> Any:
        """Trigger when invoice creation starts.

        Overwrite to create invoice with proper data, call invoice.update_invoice.
        """
        return NotImplemented

    def invoice_delete(self, invoice: "Invoice", previous_value: Any):
        """Trigger before invoice is deleted.

        Perform any extra logic before the invoice gets deleted.
        Note there is no need to run invoice.delete() as it will happen in mutation.
        """
        return NotImplemented

    def invoice_sent(self, invoice: "Invoice", email: str, previous_value: Any):
        """Trigger after invoice is sent."""
        return NotImplemented

    def account_created(self, customer: "User", previous_value: Any) -> Any:
        """Trigger when user is created.

        Overwrite this method if you need to trigger specific logic after a user is
        created.
        """
        return NotImplemented

    def order_paid(self, order: "Order", previous_value: Any) -> Any:
        """Trigger when order is paid.

        Overwrite this method if you need to trigger specific logic when an order is
        paid.
        """
        return NotImplemented

    def order_updated(self, order: "Order", previous_value: Any) -> Any:
        """Trigger when order is updated.

        Overwrite this method if you need to trigger specific logic when an order is
        changed.
        """
        return NotImplemented

    def order_cancelled(self, order: "Order", previous_value: Any) -> Any:
        """Trigger when order is cancelled.

        Overwrite this method if you need to trigger specific logic when an order is
        canceled.
        """
        return NotImplemented

    def authorize_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return NotImplemented

    def capture_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return NotImplemented

    def refund_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return NotImplemented

    def confirm_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return NotImplemented

    def process_payment(
        self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return NotImplemented

    def list_payment_sources(
        self, customer_id: str, previous_value
    ) -> List["CustomerSource"]:
        return NotImplemented

    def get_client_token(self, token_config, previous_value):
        return NotImplemented

    def get_payment_config(self, previous_value):
        return NotImplemented

    def get_supported_currencies(self, previous_value):
        return NotImplemented

    def get_payment_gateway(
        self, currency: Optional[str], previous_value
    ) -> Optional["PaymentGateway"]:
        payment_config = self.get_payment_config(previous_value)
        payment_config = payment_config if payment_config != NotImplemented else []
        currencies = self.get_supported_currencies(previous_value=[])
        currencies = currencies if currencies != NotImplemented else []
        if currency and currency not in currencies:
            return None
        return PaymentGateway(
            id=self.PLUGIN_ID,
            name=self.PLUGIN_NAME,
            config=payment_config,
            currencies=currencies,
        )

    @classmethod
    def _update_config_items(
        cls, configuration_to_update: List[dict], current_config: List[dict]
    ):
        config_structure: dict = (
            cls.CONFIG_STRUCTURE if cls.CONFIG_STRUCTURE is not None else {}
        )
        for config_item in current_config:
            for config_item_to_update in configuration_to_update:
                config_item_name = config_item_to_update.get("name")
                if config_item["name"] == config_item_name:
                    new_value = config_item_to_update.get("value")
                    item_type = config_structure.get(config_item_name, {}).get("type")
                    if (
                        item_type == ConfigurationTypeField.BOOLEAN
                        and new_value
                        and not isinstance(new_value, bool)
                    ):
                        new_value = new_value.lower() == "true"
                    config_item.update([("value", new_value)])

        # Get new keys that don't exist in current_config and extend it.
        current_config_keys = set(c_field["name"] for c_field in current_config)
        configuration_to_update_dict = {
            c_field["name"]: c_field["value"] for c_field in configuration_to_update
        }
        missing_keys = set(configuration_to_update_dict.keys()) - current_config_keys
        for missing_key in missing_keys:
            if not config_structure.get(missing_key):
                continue
            current_config.append(
                {
                    "name": missing_key,
                    "value": configuration_to_update_dict[missing_key],
                }
            )

    @classmethod
    def validate_plugin_configuration(cls, plugin_configuration: "PluginConfiguration"):
        """Validate if provided configuration is correct.

        Raise django.core.exceptions.ValidationError otherwise.
        """
        return

    @classmethod
    def save_plugin_configuration(
        cls, plugin_configuration: "PluginConfiguration", cleaned_data
    ):
        current_config = plugin_configuration.configuration
        configuration_to_update = cleaned_data.get("configuration")
        if configuration_to_update:
            cls._update_config_items(configuration_to_update, current_config)
        if "active" in cleaned_data:
            plugin_configuration.active = cleaned_data["active"]
        cls.validate_plugin_configuration(plugin_configuration)
        plugin_configuration.save()
        if plugin_configuration.configuration:
            # Let's add a translated descriptions and labels
            cls._append_config_structure(plugin_configuration.configuration)
        return plugin_configuration

    @classmethod
    def _append_config_structure(cls, configuration: PluginConfigurationType):
        """Append configuration structure to config from the database.

        Database stores "key: value" pairs, the definition of fields should be declared
        inside of the plugin. Based on this, the plugin will generate a structure of
        configuration with current values and provide access to it via API.
        """
        config_structure = getattr(cls, "CONFIG_STRUCTURE") or {}
        for configuration_field in configuration:

            structure_to_add = config_structure.get(configuration_field.get("name"))
            if structure_to_add:
                configuration_field.update(structure_to_add)

    @classmethod
    def _update_configuration_structure(cls, configuration: PluginConfigurationType):
        config_structure = getattr(cls, "CONFIG_STRUCTURE") or {}
        desired_config_keys = set(config_structure.keys())

        configured_keys = set(d["name"] for d in configuration)
        missing_keys = desired_config_keys - configured_keys

        if not missing_keys:
            return

        default_config = cls.DEFAULT_CONFIGURATION
        if not default_config:
            return

        update_values = [copy(k) for k in default_config if k["name"] in missing_keys]
        configuration.extend(update_values)

    @classmethod
    def get_default_active(cls):
        return cls.DEFAULT_ACTIVE

    def get_plugin_configuration(
        self, configuration: PluginConfigurationType
    ) -> PluginConfigurationType:
        if not configuration:
            configuration = []
        self._update_configuration_structure(configuration)
        if configuration:
            # Let's add a translated descriptions and labels
            self._append_config_structure(configuration)
        return configuration
