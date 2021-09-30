from typing import TYPE_CHECKING, Any, Dict, List, Optional

import opentracing
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.module_loading import import_string

from ..core.payments import PaymentInterface
from .models import PluginConfiguration

if TYPE_CHECKING:
    # flake8: noqa
    from .base_plugin import BasePlugin
    from ..account.models import Address, User
    from ..order.models import Order
    from ..invoice.models import Invoice
    from ..payment.interface import (
        PaymentData,
        TokenConfig,
        GatewayResponse,
        CustomerSource,
        PaymentGateway,
    )


class PluginsManager(PaymentInterface):
    """Base manager for handling plugins logic."""

    plugins: List["BasePlugin"] = []

    def __init__(self, plugins: List[str]):
        self.plugins = []
        all_configs = self._get_all_plugin_configs()
        for plugin_path in plugins:
            PluginClass = import_string(plugin_path)
            if PluginClass.PLUGIN_ID in all_configs:
                existing_config = all_configs[PluginClass.PLUGIN_ID]
                plugin_config = existing_config.configuration
                active = existing_config.active
            else:
                plugin_config = PluginClass.DEFAULT_CONFIGURATION
                active = PluginClass.get_default_active()
            self.plugins.append(PluginClass(configuration=plugin_config, active=active))

    def __run_method_on_plugins(
        self, method_name: str, default_value: Any, *args, **kwargs
    ):
        """Try to run a method with the given name on each declared plugin."""
        with opentracing.global_tracer().start_active_span(
            f"ExtensionsManager.{method_name}"
        ):
            value = default_value
            for plugin in self.plugins:
                value = self.__run_method_on_single_plugin(
                    plugin, method_name, value, *args, **kwargs
                )
            return value

    def __run_method_on_single_plugin(
        self,
        plugin: Optional["BasePlugin"],
        method_name: str,
        previous_value: Any,
        *args,
        **kwargs,
    ) -> Any:
        """Run method_name on plugin.

        Method will return value returned from plugin's
        method. If plugin doesn't have own implementation of expected method_name, it
        will return previous_value.
        """
        plugin_method = getattr(plugin, method_name, NotImplemented)
        if plugin_method == NotImplemented:
            return previous_value

        returned_value = plugin_method(*args, **kwargs, previous_value=previous_value)
        if returned_value == NotImplemented:
            return previous_value
        return returned_value

    def change_user_address(
        self, address: "Address", address_type: Optional[str], user: Optional["User"]
    ) -> "Address":
        default_value = address
        return self.__run_method_on_plugins(
            "change_user_address", default_value, address, address_type, user
        )

    def account_created(self, account: "User"):
        default_value = None
        return self.__run_method_on_plugins("account_created", default_value, account)

    def order_created(self, order: "Order"):
        default_value = None
        return self.__run_method_on_plugins("order_created", default_value, order)

    def invoice_request(
        self, order: "Order", invoice: "Invoice", number: Optional[str]
    ):
        default_value = None
        return self.__run_method_on_plugins(
            "invoice_request", default_value, order, invoice, number
        )

    def invoice_delete(self, invoice: "Invoice"):
        default_value = None
        return self.__run_method_on_plugins("invoice_delete", default_value, invoice)

    def invoice_sent(self, invoice: "Invoice", email: str):
        default_value = None
        return self.__run_method_on_plugins(
            "invoice_sent", default_value, invoice, email
        )

    def order_paid(self, order: "Order"):
        default_value = None
        return self.__run_method_on_plugins("order_paid", default_value, order)

    def order_updated(self, order: "Order"):
        default_value = None
        return self.__run_method_on_plugins("order_updated", default_value, order)

    def order_cancelled(self, order: "Order"):
        default_value = None
        return self.__run_method_on_plugins("order_cancelled", default_value, order)

    def authorize_payment(
        self, gateway: str, payment_information: "PaymentData"
    ) -> "GatewayResponse":
        method_name = "authorize_payment"
        return self.__run_payment_method(gateway, method_name, payment_information)

    def capture_payment(
        self, gateway: str, payment_information: "PaymentData"
    ) -> "GatewayResponse":
        method_name = "capture_payment"
        return self.__run_payment_method(gateway, method_name, payment_information)

    def refund_payment(
        self, gateway: str, payment_information: "PaymentData"
    ) -> "GatewayResponse":
        method_name = "refund_payment"
        return self.__run_payment_method(gateway, method_name, payment_information)

    def void_payment(
        self, gateway: str, payment_information: "PaymentData"
    ) -> "GatewayResponse":
        method_name = "void_payment"
        return self.__run_payment_method(gateway, method_name, payment_information)

    def confirm_payment(
        self, gateway: str, payment_information: "PaymentData"
    ) -> "GatewayResponse":
        method_name = "confirm_payment"
        return self.__run_payment_method(gateway, method_name, payment_information)

    def process_payment(
        self, gateway: str, payment_information: "PaymentData"
    ) -> "GatewayResponse":
        method_name = "process_payment"
        return self.__run_payment_method(gateway, method_name, payment_information)

    def get_client_token(self, gateway, token_config: "TokenConfig") -> str:
        method_name = "get_client_token"
        default_value = None
        gtw = self.get_plugin(gateway)
        return self.__run_method_on_single_plugin(
            gtw, method_name, default_value, token_config=token_config
        )

    def list_payment_sources(
        self, gateway: str, customer_id: str
    ) -> List["CustomerSource"]:
        default_value: list = []
        gtw = self.get_plugin(gateway)
        if gtw is not None:
            return self.__run_method_on_single_plugin(
                gtw, "list_payment_sources", default_value, customer_id=customer_id
            )
        raise Exception(f"Payment plugin {gateway} is inaccessible!")

    def get_active_plugins(self, plugins=None) -> List["BasePlugin"]:
        if plugins is None:
            plugins = self.plugins
        return [plugin for plugin in plugins if plugin.active]

    def list_payment_plugin(self, active_only: bool = False) -> Dict[str, "BasePlugin"]:
        payment_method = "process_payment"
        plugins = self.plugins
        if active_only:
            plugins = self.get_active_plugins()
        return {
            plugin.PLUGIN_ID: plugin
            for plugin in plugins
            if payment_method in type(plugin).__dict__
        }

    def list_payment_gateways(
        self, currency: Optional[str] = None, active_only: bool = True
    ) -> List["PaymentGateway"]:
        payment_plugins = self.list_payment_plugin(active_only=active_only)
        # if currency is given return only gateways which support given currency
        gateways = []
        for plugin in payment_plugins.values():
            gateway = plugin.get_payment_gateway(currency=currency, previous_value=None)
            if gateway:
                gateways.append(gateway)
        return gateways

    def __run_payment_method(
        self,
        gateway: str,
        method_name: str,
        payment_information: "PaymentData",
        **kwargs,
    ) -> "GatewayResponse":
        default_value = None
        gtw = self.get_plugin(gateway)
        if gtw is not None:
            resp = self.__run_method_on_single_plugin(
                gtw,
                method_name,
                previous_value=default_value,
                payment_information=payment_information,
                **kwargs,
            )
            if resp is not None:
                return resp

        raise Exception(
            f"Payment plugin {gateway} for {method_name}"
            " payment method is inaccessible!"
        )

    def _get_all_plugin_configs(self):
        if not hasattr(self, "_plugin_configs"):
            self._plugin_configs = {
                pc.identifier: pc for pc in PluginConfiguration.objects.all()
            }
        return self._plugin_configs

    # FIXME these methods should be more generic

    def save_plugin_configuration(self, plugin_id, cleaned_data: dict):
        for plugin in self.plugins:
            if plugin.PLUGIN_ID == plugin_id:
                plugin_configuration, _ = PluginConfiguration.objects.get_or_create(
                    identifier=plugin_id,
                    defaults={"configuration": plugin.configuration},
                )
                return plugin.save_plugin_configuration(
                    plugin_configuration, cleaned_data
                )

    def get_plugin(self, plugin_id: str) -> Optional["BasePlugin"]:
        for plugin in self.plugins:
            if plugin.PLUGIN_ID == plugin_id:
                return plugin
        return None

    def fetch_taxes_data(self) -> bool:
        default_value = False
        return self.__run_method_on_plugins("fetch_taxes_data", default_value)

    def webhook(self, request: WSGIRequest, plugin_id: str) -> HttpResponse:
        split_path = request.path.split(plugin_id, maxsplit=1)
        path = None
        if len(split_path) == 2:
            path = split_path[1]

        default_value = HttpResponseNotFound()
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            return default_value
        return self.__run_method_on_single_plugin(
            plugin, "webhook", default_value, request, path
        )


def get_plugins_manager(
    manager_path: str = None, plugins: List[str] = None
) -> PluginsManager:
    if not manager_path:
        manager_path = settings.PLUGINS_MANAGER
    if plugins is None:
        plugins = settings.PLUGINS
    manager = import_string(manager_path)
    return manager(plugins)
