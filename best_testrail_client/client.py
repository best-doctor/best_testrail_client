from __future__ import annotations

from json import JSONDecodeError

import requests
import typing

from best_testrail_client.custom_types import (
    ModelID, Method, JsonData, DeleteResult, CreatedFilters, StatusFilters, AttachmentFile,
)
from best_testrail_client.exceptions import TestRailException
from best_testrail_client.models.attachment import Attachment
from best_testrail_client.models.case_types import CaseType
from best_testrail_client.models.configuration import Configuration, GroupConfig
from best_testrail_client.models.priority import Priority
from best_testrail_client.models.result import Result
from best_testrail_client.models.result_fields import ResultFields
from best_testrail_client.models.run import Run
from best_testrail_client.models.section import Section
from best_testrail_client.models.status import Status
from best_testrail_client.models.template import Template
from best_testrail_client.models.user import User
from best_testrail_client.utils import convert_list_to_filter


class TestRailClient:
    """http://docs.gurock.com/testrail-api2/start"""
    def __init__(self, testrail_url: str, login: str, token: str):
        self.token = token
        self.login = login
        self.project_id: typing.Optional[ModelID] = None

        if not testrail_url.endswith('/'):
            testrail_url += '/'
        self.base_url = f'{testrail_url}index.php?/api/v2/'

    # Custom methods
    def set_project_id(self, project_id: ModelID) -> TestRailClient:
        self.project_id = project_id
        return self

    # Attachments API  http://docs.gurock.com/testrail-api2/reference-attachments
    def add_attachment_to_result(
        self, result_id: ModelID, attachment_file: AttachmentFile,
    ) -> typing.Optional[ModelID]:
        """http://docs.gurock.com/testrail-api2/reference-attachments#add_attachment_to_result"""
        attachment_data = self.__request(
            f'add_attachment_to_result/{result_id}', method='POST', attachment=attachment_file,
        )
        return attachment_data.get('attachment_id')

    def get_attachments_for_case(self, case_id: ModelID) -> typing.List[Attachment]:
        """http://docs.gurock.com/testrail-api2/reference-attachments#get_attachments_for_case"""
        attachments_data = self.__request(f'get_attachments_for_case/{case_id}')
        return [
            Attachment.from_json(data_json=attachment_data) for attachment_data in attachments_data
        ]

    def get_attachments_for_test(self, test_id: ModelID) -> typing.List[Attachment]:
        """http://docs.gurock.com/testrail-api2/reference-attachments#get_attachments_for_test"""
        attachments_data = self.__request(f'get_attachments_for_test/{test_id}')
        return [
            Attachment.from_json(data_json=attachment_data) for attachment_data in attachments_data
        ]

    def get_attachment(self, attachment_id: ModelID) -> Attachment:
        """http://docs.gurock.com/testrail-api2/reference-attachments#get_attachment"""
        attachment_data = self.__request(f'get_attachment/{attachment_id}')
        return Attachment.from_json(data_json=attachment_data)

    def delete_attachment(self, attachment_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-attachments#delete_attachment"""
        self.__request(f'delete_attachment/{attachment_id}', method='POST')
        return True

    # Case Types API  http://docs.gurock.com/testrail-api2/reference-cases-types
    def get_case_types(self) -> typing.List[CaseType]:
        case_types_data = self.__request('get_case_types')
        return [CaseType.from_json(case_type) for case_type in case_types_data]

    # Configurations API  http://docs.gurock.com/testrail-api2/reference-configs
    def get_configs(
        self, project_id: typing.Optional[ModelID] = None,
    ) -> typing.List[Configuration]:
        """http://docs.gurock.com/testrail-api2/reference-configs#get_configs"""
        project_id = project_id or self.project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        configurations_data = self.__request(f'get_configs/{project_id}')
        return [
            Configuration.from_json(configuration_data)
            for configuration_data in configurations_data
        ]

    def add_config_group(
        self, name: str, project_id: typing.Optional[ModelID] = None,
    ) -> Configuration:
        """http://docs.gurock.com/testrail-api2/reference-configs#add_config_group"""
        new_config_group_data = {'name': name}
        project_id = project_id or self.project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        config_group_data = self.__request(
            f'add_config_group/{project_id}', method='POST', data=new_config_group_data,
        )
        return Configuration.from_json(config_group_data)

    def add_config(self, name: str, config_group_id: ModelID) -> GroupConfig:
        """http://docs.gurock.com/testrail-api2/reference-configs#add_config"""
        new_config_data = {'name': name}
        config_group_data = self.__request(
            f'add_config/{config_group_id}', method='POST', data=new_config_data,
        )
        return GroupConfig.from_json(config_group_data)

    def update_config_group(self, name: str, config_group_id: ModelID) -> Configuration:
        """http://docs.gurock.com/testrail-api2/reference-configs#update_config_group"""
        new_config_group_data = {'name': name}
        config_group_data = self.__request(
            f'update_config_group/{config_group_id}', method='POST', data=new_config_group_data,
        )
        return Configuration.from_json(config_group_data)

    def update_config(self, name: str, config_id: ModelID) -> GroupConfig:
        """http://docs.gurock.com/testrail-api2/reference-configs#update_config"""
        new_config_data = {'name': name}
        config_data = self.__request(
            f'update_config/{config_id}', method='POST', data=new_config_data,
        )
        return GroupConfig.from_json(config_data)

    def delete_config_group(self, config_group_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-configs#delete_config_group"""
        self.__request(f'delete_config_group/{config_group_id}', method='POST')
        return True

    def delete_config(self, config_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-configs#delete_config"""
        self.__request(f'delete_config/{config_id}', method='POST')
        return True

    # Priorities API  http://docs.gurock.com/testrail-api2/reference-priorities
    def get_priorities(self) -> typing.List[Priority]:
        """http://docs.gurock.com/testrail-api2/reference-priorities#get_priorities"""
        priorities_data = self.__request('get_priorities')
        return [Priority.from_json(priority) for priority in priorities_data]

    # Results API  http://docs.gurock.com/testrail-api2/reference-results
    def get_results(
        self,
        test_id: ModelID,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
        status_ids: typing.Optional[typing.List[int]] = None,
    ) -> typing.List[Result]:
        """http://docs.gurock.com/testrail-api2/reference-results#get_results"""
        status = ','.join(str(status) for status in status_ids) if status_ids is not None else ''
        filters = {
            'limit': limit,
            'offset': offset,
            'status_id': status,
        }
        results_data = self.__request(f'get_results/{test_id}', params=filters)
        return [Result.from_json(result_data) for result_data in results_data]

    def get_results_for_case(
        self,
        run_id: ModelID,
        case_id: ModelID,
        filters: typing.Optional[StatusFilters] = None,
    ) -> typing.List[Result]:
        """http://docs.gurock.com/testrail-api2/reference-results#get_results_for_case"""
        params: JsonData = {}
        if filters is not None:
            params = {
                'limit': filters.get('limit'),
                'offset': filters.get('offset'),
                'status_id': convert_list_to_filter(values_list=filters.get('status_ids')),
            }
        results_data = self.__request(f'get_results_for_case/{run_id}/{case_id}', params=params)
        return [Result.from_json(result_data) for result_data in results_data]

    def get_results_for_run(
        self,
        run_id: ModelID,
        filters: typing.Optional[CreatedFilters] = None,
    ) -> typing.List[Result]:
        """http://docs.gurock.com/testrail-api2/reference-results#get_results_for_run"""
        params: JsonData = {}
        if filters is not None:
            params = {
                'created_after': filters.get('created_after'),
                'created_before': filters.get('created_before'),
                'created_by': convert_list_to_filter(values_list=filters.get('created_by')),
                'limit': filters.get('limit'),
                'offset': filters.get('offset'),
                'status_id': convert_list_to_filter(values_list=filters.get('status_ids')),
            }
        results_data = self.__request(f'get_results_for_run/{run_id}', params=params)
        return [Result.from_json(result_data) for result_data in results_data]

    def add_result(self, test_id: ModelID, result: Result) -> Result:
        """http://docs.gurock.com/testrail-api2/reference-results#add_result"""
        new_result_data = result.to_json()
        result_data = self.__request(f'add_result/{test_id}', method='POST', data=new_result_data)
        return Result.from_json(data_json=result_data)

    def add_result_for_case(self, run_id: ModelID, case_id: ModelID, result: Result) -> Result:
        """http://docs.gurock.com/testrail-api2/reference-results#add_result_for_case"""
        new_result_data = result.to_json()
        result_data = self.__request(
            f'add_result_for_case/{run_id}/{case_id}', method='POST', data=new_result_data,
        )
        return Result.from_json(data_json=result_data)

    def add_results(self, run_id: ModelID, results: typing.List[Result]) -> typing.List[Result]:
        """http://docs.gurock.com/testrail-api2/reference-results#add_results"""
        new_results_data = {
            'results': [result.to_json() for result in results],
        }
        results_data = self.__request(
            f'add_results/{run_id}', method='POST', data=new_results_data,
        )
        return [Result.from_json(data_json=result_data) for result_data in results_data]

    def add_results_for_cases(
        self, run_id: ModelID, results: typing.List[Result],
    ) -> typing.List[Result]:
        """http://docs.gurock.com/testrail-api2/reference-results#add_results_for_cases"""
        new_results_data = {
            'results': [result.to_json() for result in results],
        }
        results_data = self.__request(
            f'add_results_for_cases/{run_id}', method='POST', data=new_results_data,
        )
        return [Result.from_json(data_json=result_data) for result_data in results_data]

    # Result Fields API  http://docs.gurock.com/testrail-api2/reference-results-fields
    def get_result_fields(self) -> typing.List[ResultFields]:
        """http://docs.gurock.com/testrail-api2/reference-results-fields#get_result_fields"""
        result_fields_data = self.__request('get_result_fields')
        return [ResultFields.from_json(result_fields) for result_fields in result_fields_data]

    # Runs API  http://docs.gurock.com/testrail-api2/reference-runs
    def get_run(self, run_id: ModelID) -> Run:
        """http://docs.gurock.com/testrail-api2/reference-runs#get_run"""
        run_data = self.__request(f'get_run/{run_id}')
        return Run.from_json(data_json=run_data)

    def get_runs(self, project_id: typing.Optional[ModelID] = None) -> typing.List[Run]:
        """http://docs.gurock.com/testrail-api2/reference-runs#get_runs"""
        project_id = project_id or self.project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        runs_data = self.__request(f'get_runs/{project_id}')
        return [Run.from_json(data_json=run_data) for run_data in runs_data]

    def add_run(self, run: Run, project_id: typing.Optional[ModelID] = None) -> Run:
        """http://docs.gurock.com/testrail-api2/reference-runs#add_run"""
        project_id = project_id or self.project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        new_run_data = run.to_json(include_none=False)
        run_data = self.__request(f'add_run/{project_id}', method='POST', data=new_run_data)
        return Run.from_json(data_json=run_data)

    def update_run(self, updated_run: Run) -> Run:
        """http://docs.gurock.com/testrail-api2/reference-runs#update_run"""
        update_run_data = updated_run.to_json(include_none=False)
        run_data = self.__request(
            f'update_run/{updated_run.id}', method='POST', data=update_run_data,
        )
        return Run.from_json(data_json=run_data)

    def close_run(self, run_id: ModelID) -> Run:
        """http://docs.gurock.com/testrail-api2/reference-runs#close_run"""
        run_data = self.__request(f'close_run/{run_id}', method='POST')
        return Run.from_json(data_json=run_data)

    def delete_run(self, run_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-runs#delete_run"""
        self.__request(f'delete_run/{run_id}', method='POST')
        return True

    # Sections API  http://docs.gurock.com/testrail-api2/reference-sections
    def get_section(self, section_id: ModelID) -> Section:
        """http://docs.gurock.com/testrail-api2/reference-sections#get_section"""
        section_data = self.__request(f'get_section/{section_id}')
        return Section.from_json(section_data)

    def get_sections(
        self,
        project_id: typing.Optional[ModelID] = None, suite_id: typing.Optional[ModelID] = None,
    ) -> typing.List[Section]:
        """http://docs.gurock.com/testrail-api2/reference-sections#get_sections"""
        project_id = project_id or self.project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        sections_data = self.__request(f'get_sections/{project_id}', params={'suite_id': suite_id})
        return [Section.from_json(section) for section in sections_data]

    def add_section(self, section: Section, project_id: typing.Optional[ModelID] = None) -> Section:
        """http://docs.gurock.com/testrail-api2/reference-sections#add_section"""
        project_id = project_id or self.project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        new_section_data = section.to_json(include_none=False)
        section_data = self.__request(
            f'add_section/{project_id}', method='POST', data=new_section_data,
        )
        return Section.from_json(section_data)

    def update_section(
        self, section_id: ModelID, name: str, description: typing.Optional[str] = None,
    ) -> Section:
        """http://docs.gurock.com/testrail-api2/reference-sections#update_section"""
        new_section_data = {'name': name}
        if description is not None:
            new_section_data['description'] = description
        section_data = self.__request(
            f'update_section/{section_id}', method='POST', data=new_section_data,
        )
        return Section.from_json(section_data)

    def delete_section(self, section_id: ModelID) -> DeleteResult:
        """http://docs.gurock.com/testrail-api2/reference-sections#delete_section"""
        self.__request(f'delete_section/{section_id}', method='POST')
        return True

    # Statuses API  http://docs.gurock.com/testrail-api2/reference-statuses
    def get_statuses(self) -> typing.List[Status]:
        """http://docs.gurock.com/testrail-api2/reference-statuses#get_statuses"""
        statuses_data = self.__request('get_statuses')
        return [Status.from_json(status) for status in statuses_data]

    # Templates API  http://docs.gurock.com/testrail-api2/reference-templates
    def get_templates(self, project_id: typing.Optional[ModelID] = None) -> typing.List[Template]:
        """http://docs.gurock.com/testrail-api2/reference-templates#get_templates"""
        project_id = project_id or self.project_id
        if project_id is None:
            raise TestRailException('Provide project id')
        templates_data = self.__request(f'get_templates/{project_id}')
        return [Template.from_json(template) for template in templates_data]

    # Users API  http://docs.gurock.com/testrail-api2/reference-users
    def get_user(self, user_id: ModelID) -> User:
        """http://docs.gurock.com/testrail-api2/reference-users#get_user"""
        user_data = self.__request(f'get_user/{user_id}')
        return User.from_json(user_data)

    def get_user_by_email(self, email: str) -> User:
        """http://docs.gurock.com/testrail-api2/reference-users#get_user_by_email"""
        user_data = self.__request(f'get_user_by_email/{email}')
        return User.from_json(user_data)

    def get_users(self) -> typing.List[User]:
        """http://docs.gurock.com/testrail-api2/reference-users#get_users"""
        users_data: typing.List[JsonData] = self.__request('get_users')
        return [User.from_json(user_data) for user_data in users_data]

    def __request(
        self,
        url: str, data: typing.Optional[JsonData] = None, method: Method = 'GET',
        params: typing.Optional[JsonData] = None,
        attachment: typing.Optional[AttachmentFile] = None,
    ) -> typing.Any:
        if data is None:
            data = {}
        attach_files = None
        if attachment is not None:
            attach_files = {'attachment': (attachment['name'], attachment['file_content'])}

        response = requests.request(
            method, f'{self.base_url}{url}', json=data,
            auth=(self.login, self.token), params=params, files=attach_files,
        )

        try:
            return response.json()
        except JSONDecodeError:
            return response
