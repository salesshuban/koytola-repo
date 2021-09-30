import json

import pytest

from ..schema.email import (
    get_order_confirmation_markup,
    get_organization,
)


def test_get_organization(site_settings):
    example_name = "Site Name"
    site = site_settings.site
    site.name = example_name
    site.save()

    result = get_organization()
    assert result["name"] == example_name


def test_get_order_confirmation_markup(order_with_lines):
    try:
        result = get_order_confirmation_markup(order_with_lines)
    except TypeError:
        pytest.fail("Function output is not JSON serializable")

    try:
        # Response should be returned as a valid json
        json.loads(result)
    except ValueError:
        pytest.fail("Response is not a valid json")
