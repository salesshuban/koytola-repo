from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from ..base_plugin import BasePlugin, ConfigurationTypeField


class PluginSample(BasePlugin):
    PLUGIN_ID = "plugin.sample"
    PLUGIN_NAME = "PluginSample"
    PLUGIN_DESCRIPTION = "Test plugin description"
    DEFAULT_ACTIVE = True
    DEFAULT_CONFIGURATION = [
        {"name": "Username", "value": "admin"},
        {"name": "Password", "value": None},
        {"name": "Use sandbox", "value": False},
        {"name": "API private key", "value": None},
    ]

    CONFIG_STRUCTURE = {
        "Username": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "Username input field",
            "label": "Username",
        },
        "Password": {
            "type": ConfigurationTypeField.PASSWORD,
            "help_text": "Password input field",
            "label": "Password",
        },
        "Use sandbox": {
            "type": ConfigurationTypeField.BOOLEAN,
            "help_text": "Use sandbox",
            "label": "Use sandbox",
        },
        "API private key": {
            "type": ConfigurationTypeField.SECRET,
            "help_text": "API key",
            "label": "Private key",
        },
    }

    def webhook(self, request: WSGIRequest, path: str, previous_value) -> HttpResponse:
        if path == "/webhook/paid":
            return JsonResponse(data={"received": True, "paid": True})
        if path == "/webhook/failed":
            return JsonResponse(data={"received": True, "paid": False})
        return HttpResponseNotFound()


class PluginInactive(BasePlugin):
    PLUGIN_ID = "plugin.inactive"
    PLUGIN_NAME = "PluginInactive"
    PLUGIN_DESCRIPTION = "Test plugin description_2"


class ActivePlugin(BasePlugin):
    PLUGIN_ID = "plugin.active"
    PLUGIN_NAME = "Active"
    PLUGIN_DESCRIPTION = "Not working"
    DEFAULT_ACTIVE = True


class ActivePaymentGateway(BasePlugin):
    PLUGIN_ID = "gateway.active"
    CLIENT_CONFIG = [
        {"field": "foo", "value": "bar"},
    ]
    PLUGIN_NAME = "braintree"
    DEFAULT_ACTIVE = True
    SUPPORTED_CURRENCIES = ["USD"]

    def process_payment(self, payment_information, previous_value):
        pass

    def get_supported_currencies(self, previous_value):
        return self.SUPPORTED_CURRENCIES

    def get_payment_config(self, previous_value):
        return self.CLIENT_CONFIG


class ActiveDummyPaymentGateway(BasePlugin):
    PLUGIN_ID = "sampleDummy.active"
    CLIENT_CONFIG = [
        {"field": "foo", "value": "bar"},
    ]
    PLUGIN_NAME = "SampleDummy"
    DEFAULT_ACTIVE = True
    SUPPORTED_CURRENCIES = ["PLN", "USD"]

    def process_payment(self, payment_information, previous_value):
        pass

    def get_supported_currencies(self, previous_value):
        return self.SUPPORTED_CURRENCIES

    def get_payment_config(self, previous_value):
        return self.CLIENT_CONFIG


class InactivePaymentGateway(BasePlugin):
    PLUGIN_ID = "gateway.inactive"
    PLUGIN_NAME = "stripe"

    def process_payment(self, payment_information, previous_value):
        pass
