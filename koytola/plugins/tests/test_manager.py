import json
from django.http import HttpResponseNotFound, JsonResponse
from ...payment.interface import PaymentGateway
from ..manager import PluginsManager, get_plugins_manager
from ..models import PluginConfiguration
from ..tests.sample_plugins import (
    ActiveDummyPaymentGateway,
    ActivePaymentGateway,
    InactivePaymentGateway,
    PluginInactive,
    PluginSample,
)


def test_get_plugins_manager():
    manager_path = "koytola.plugins.manager.PluginsManager"
    plugin_path = "koytola.plugins.tests.sample_plugins.PluginSample"
    manager = get_plugins_manager(manager_path=manager_path, plugins=[plugin_path])
    assert isinstance(manager, PluginsManager)
    assert len(manager.plugins) == 1


def test_manager_get_plugin_configurations(plugin_configuration):
    plugins = [
        "koytola.plugins.tests.sample_plugins.PluginSample",
        "koytola.plugins.tests.sample_plugins.PluginInactive",
    ]
    manager = PluginsManager(plugins=plugins)
    plugin_configs = manager._plugin_configs.values()
    assert len(plugin_configs) == 1
    assert set(plugin_configs) == set(list(PluginConfiguration.objects.all()))


def test_manager_get_plugin_configuration(plugin_configuration):
    plugins = [
        "koytola.plugins.tests.sample_plugins.PluginSample",
        "koytola.plugins.tests.sample_plugins.PluginInactive",
    ]
    manager = PluginsManager(plugins=plugins)
    plugin = manager.get_plugin(PluginSample.PLUGIN_ID)
    configuration_from_db = PluginConfiguration.objects.get(
        identifier=PluginSample.PLUGIN_ID
    )
    assert plugin.DEFAULT_CONFIGURATION == configuration_from_db.configuration


def test_manager_save_plugin_configuration(plugin_configuration):
    plugins = ["koytola.plugins.tests.sample_plugins.PluginSample"]
    manager = PluginsManager(plugins=plugins)
    manager.save_plugin_configuration(PluginSample.PLUGIN_ID, {"active": False})
    plugin_configuration.refresh_from_db()
    assert not plugin_configuration.active


def test_plugin_updates_configuration_shape(
    new_config, new_config_structure, plugin_configuration, monkeypatch,
):

    config_structure = PluginSample.CONFIG_STRUCTURE.copy()
    config_structure["Foo"] = new_config_structure
    monkeypatch.setattr(PluginSample, "CONFIG_STRUCTURE", config_structure)

    monkeypatch.setattr(
        PluginSample,
        "DEFAULT_CONFIGURATION",
        plugin_configuration.configuration + [new_config],
    )

    manager = PluginsManager(
        plugins=["koytola.plugins.tests.sample_plugins.PluginSample"]
    )
    plugin = manager.get_plugin(PluginSample.PLUGIN_ID)

    assert len(plugin.configuration) == 5
    assert plugin.configuration[-1] == {**new_config, **new_config_structure}


def test_plugin_add_new_configuration(
    new_config, new_config_structure, monkeypatch,
):
    monkeypatch.setattr(PluginInactive, "DEFAULT_ACTIVE", True)
    monkeypatch.setattr(
        PluginInactive, "DEFAULT_CONFIGURATION", [new_config],
    )
    config_structure = {"Foo": new_config_structure}
    monkeypatch.setattr(PluginInactive, "CONFIG_STRUCTURE", config_structure)
    manager = PluginsManager(
        plugins=["koytola.plugins.tests.sample_plugins.PluginInactive"]
    )
    plugin = manager.get_plugin(PluginInactive.PLUGIN_ID)
    assert len(plugin.configuration) == 1
    assert plugin.configuration[0] == {**new_config, **new_config_structure}


def test_manager_serve_list_of_payment_gateways():
    expected_gateway = PaymentGateway(
        id=ActivePaymentGateway.PLUGIN_ID,
        name=ActivePaymentGateway.PLUGIN_NAME,
        config=ActivePaymentGateway.CLIENT_CONFIG,
        currencies=ActivePaymentGateway.SUPPORTED_CURRENCIES,
    )
    plugins = [
        "koytola.plugins.tests.sample_plugins.PluginSample",
        "koytola.plugins.tests.sample_plugins.ActivePaymentGateway",
        "koytola.plugins.tests.sample_plugins.InactivePaymentGateway",
    ]
    manager = PluginsManager(plugins=plugins)
    assert manager.list_payment_gateways() == [expected_gateway]


def test_manager_serve_list_all_payment_gateways():
    expected_gateways = [
        PaymentGateway(
            id=ActivePaymentGateway.PLUGIN_ID,
            name=ActivePaymentGateway.PLUGIN_NAME,
            config=ActivePaymentGateway.CLIENT_CONFIG,
            currencies=ActivePaymentGateway.SUPPORTED_CURRENCIES,
        ),
        PaymentGateway(
            id=InactivePaymentGateway.PLUGIN_ID,
            name=InactivePaymentGateway.PLUGIN_NAME,
            config=[],
            currencies=[],
        ),
    ]

    plugins = [
        "koytola.plugins.tests.sample_plugins.ActivePaymentGateway",
        "koytola.plugins.tests.sample_plugins.InactivePaymentGateway",
    ]
    manager = PluginsManager(plugins=plugins)
    assert manager.list_payment_gateways(active_only=False) == expected_gateways


def test_manager_serve_list_all_payment_gateways_specified_currency():
    expected_gateways = [
        PaymentGateway(
            id=ActiveDummyPaymentGateway.PLUGIN_ID,
            name=ActiveDummyPaymentGateway.PLUGIN_NAME,
            config=ActiveDummyPaymentGateway.CLIENT_CONFIG,
            currencies=ActiveDummyPaymentGateway.SUPPORTED_CURRENCIES,
        )
    ]

    plugins = [
        "koytola.plugins.tests.sample_plugins.ActivePaymentGateway",
        "koytola.plugins.tests.sample_plugins.InactivePaymentGateway",
        "koytola.plugins.tests.sample_plugins.ActiveDummyPaymentGateway",
    ]
    manager = PluginsManager(plugins=plugins)
    assert (
        manager.list_payment_gateways(currency="PLN", active_only=False)
        == expected_gateways
    )


def test_manager_serve_list_all_payment_gateways_specified_currency_two_gateways():
    expected_gateways = [
        PaymentGateway(
            id=ActivePaymentGateway.PLUGIN_ID,
            name=ActivePaymentGateway.PLUGIN_NAME,
            config=ActivePaymentGateway.CLIENT_CONFIG,
            currencies=ActivePaymentGateway.SUPPORTED_CURRENCIES,
        ),
        PaymentGateway(
            id=ActiveDummyPaymentGateway.PLUGIN_ID,
            name=ActiveDummyPaymentGateway.PLUGIN_NAME,
            config=ActiveDummyPaymentGateway.CLIENT_CONFIG,
            currencies=ActiveDummyPaymentGateway.SUPPORTED_CURRENCIES,
        ),
    ]

    plugins = [
        "koytola.plugins.tests.sample_plugins.ActivePaymentGateway",
        "koytola.plugins.tests.sample_plugins.InactivePaymentGateway",
        "koytola.plugins.tests.sample_plugins.ActiveDummyPaymentGateway",
    ]
    manager = PluginsManager(plugins=plugins)
    assert (
        manager.list_payment_gateways(currency="USD", active_only=False)
        == expected_gateways
    )


def test_manager_webhook(rf):
    plugins = [
        "koytola.plugins.tests.sample_plugins.PluginSample",
        "koytola.plugins.tests.sample_plugins.PluginInactive",
    ]
    manager = PluginsManager(plugins=plugins)
    plugin_path = "/webhook/paid"
    request = rf.post(path=f"/plugins/{PluginSample.PLUGIN_ID}{plugin_path}")

    response = manager.webhook(request, PluginSample.PLUGIN_ID)
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    assert response.content.decode() == json.dumps({"received": True, "paid": True})


def test_manager_webhook_plugin_doesnt_have_webhook_support(rf):
    plugins = [
        "koytola.plugins.tests.sample_plugins.PluginInactive",
    ]

    manager = PluginsManager(plugins=plugins)
    plugin_path = "/webhook/paid"
    request = rf.post(path=f"/plugins/{PluginInactive.PLUGIN_ID}{plugin_path}")
    response = manager.webhook(request, PluginSample.PLUGIN_ID)
    assert isinstance(response, HttpResponseNotFound)
    assert response.status_code == 404


def test_manager_inncorrect_plugin(rf):
    plugins = [
        "koytola.plugins.tests.sample_plugins.PluginSample",
        "koytola.plugins.tests.sample_plugins.PluginInactive",
    ]
    manager = PluginsManager(plugins=plugins)
    plugin_path = "/webhook/paid"
    request = rf.post(path=f"/plugins/incorrect.plugin.id{plugin_path}")
    response = manager.webhook(request, "incorrect.plugin.id")
    assert isinstance(response, HttpResponseNotFound)
    assert response.status_code == 404
