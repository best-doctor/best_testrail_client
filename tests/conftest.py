import pytest

from best_testrail_client.models.status import Status
from best_testrail_client.models.template import Template
from best_testrail_client.models.user import User


@pytest.fixture
def user_data():
    return {
        'email': 'alexis@example.com',
        'id': 1,
        'is_active': True,
        'name': 'Alexis Gonzalez',
    }


@pytest.fixture
def user(user_data):
    return User.from_json(data_json=user_data)


@pytest.fixture
def template_data():
    return {
        'id': 1,
        'is_default': True,
        'name': 'Test Case (Text)',
    }


@pytest.fixture
def template(template_data):
    return Template.from_json(data_json=template_data)


@pytest.fixture
def status_data():
    return {
        'color_bright': 12709313,
        'color_dark': 6667107,
        'color_medium': 9820525,
        'id': 1,
        'is_final': True,
        'is_system': True,
        'is_untested': False,
        'label': 'Passed',
        'name': 'passed',
    }


@pytest.fixture
def status(status_data):
    return Status.from_json(data_json=status_data)
