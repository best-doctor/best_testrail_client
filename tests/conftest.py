import pytest

from best_testrail_client.models.case_types import CaseType
from best_testrail_client.models.configuration import Configuration, GroupConfig
from best_testrail_client.models.priority import Priority
from best_testrail_client.models.result_fields import ResultFields
from best_testrail_client.models.section import Section
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


@pytest.fixture
def section_data():
    return {
        'depth': 0,
        'description': None,
        'display_order': 1,
        'id': 1,
        'name': 'Prerequisites',
        'parent_id': None,
        'suite_id': 1,
    }


@pytest.fixture
def section(section_data):
    return Section.from_json(data_json=section_data)


@pytest.fixture
def result_fields_data():
    return {
        'configs': [
            {
                'context': {
                    'is_global': True,
                    'project_ids': None,
                },
                'id': 1,
                'options': {
                    'format': 'markdown',
                    'has_actual': False,
                    'has_expected': True,
                    'is_required': False,
                },
            },
        ],
        'description': None,
        'display_order': 1,
        'id': 5,
        'label': 'Steps',
        'name': 'step_results',
        'system_name': 'custom_step_results',
        'type_id': 11,
    }


@pytest.fixture
def result_fields(result_fields_data):
    return ResultFields.from_json(data_json=result_fields_data)


@pytest.fixture
def case_types_data():
    return {
        'id': 1,
        'is_default': False,
        'name': 'Automated',
    }


@pytest.fixture
def case_types(case_types_data):
    return CaseType.from_json(data_json=case_types_data)


@pytest.fixture
def group_config_data():
    return {
        'group_id': 1,
        'id': 1,
        'name': 'Chrome',
    }


@pytest.fixture
def group_config(group_config_data):
    return GroupConfig.from_json(data_json=group_config_data)


@pytest.fixture
def configuration_data():
    return {
        'configs': [
            {
                'group_id': 1,
                'id': 1,
                'name': 'Chrome',
            },
            {
                'group_id': 1,
                'id': 2,
                'name': 'Firefox',
            },
            {
                'group_id': 1,
                'id': 3,
                'name': 'Internet Explorer',
            },
        ],
        'id': 1,
        'name': 'Browsers',
        'project_id': 1,
    }


@pytest.fixture
def configuration(configuration_data):
    return Configuration.from_json(data_json=configuration_data)


@pytest.fixture
def priority_data():
    return {
        'id': 1,
        'is_default': False,
        'name': "1 - Don't Test",
        'priority': 1,
        'short_name': "1 - Don't",
    }


@pytest.fixture
def priority(priority_data):
    return Priority.from_json(data_json=priority_data)
