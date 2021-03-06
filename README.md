# TestRail client by BestDoctor

[![Build Status](https://travis-ci.org/best-doctor/best_testrail_client.svg?branch=master)](https://travis-ci.org/best-doctor/best_testrail_client)
[![Maintainability](https://api.codeclimate.com/v1/badges/62075568c990aa8677c4/maintainability)](https://codeclimate.com/github/best-doctor/best_testrail_client/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/62075568c990aa8677c4/test_coverage)](https://codeclimate.com/github/best-doctor/best_testrail_client/test_coverage)
[![PyPI version](https://badge.fury.io/py/best-testrail-client.svg)](https://badge.fury.io/py/best-testrail-client)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/best-testrail-client)](https://pypi.org/project/best-testrail-client/)

Implements [API v2](http://docs.gurock.com/testrail-api2/start) for [TestRail](https://www.gurock.com/testrail/).

## Installation

```bash
pip install best_testrail_client
```

## Prerequisites

1. Enabled API in your TestRail project.

    ![Enable TestRail API](https://raw.githubusercontent.com/best-doctor/best_testrail_client/master/docs_img/enable_API.png)
1. Generated API key.

    ![Generate API key](https://raw.githubusercontent.com/best-doctor/best_testrail_client/master/docs_img/API_key.png)

## Usage

```python
from best_testrail_client.client import TestRailClient
from best_testrail_client.enums import BaseResultStatus
from best_testrail_client.models.result import Result
from best_testrail_client.models.run import Run

# Client initialization
project_url = 'https://<YOUR_PROJECT>.testrail.io/'  # or other URL for self-hosted
login = '<account email>'
api_token = '<generated API token>'

client = TestRailClient(project_url, login, api_token)

# Create Test Run
new_run = Run(
    name='Test Run from API',
    include_all=False,
    case_ids=[1, 2, 3],
)
created_run = client.runs.add_run(run=new_run, project_id=1)

# You can set global Project ID
client.set_project_id(project_id=2)

# Add results for run
results = [
    Result(status_id=BaseResultStatus.PASSED.value, case_id=1, comment='Passed test'),
    Result(status_id=BaseResultStatus.FAILED.value, case_id=2, comment='Failed test'),
    Result(status_id=6, case_id=3, comment='Waiting test'),  # Custom status
]
client.results.add_results_for_cases(run_id=created_run.id, results=results)

# Close run
client.runs.close_run(run_id=created_run.id)
```

### Custom attributes

Custom attributes are stored in `custom` dictionary attribute in models.
It stores all data from API and converts it back.

```python
from best_testrail_client.client import TestRailClient

# Client initialization
project_url = 'https://<YOUR_PROJECT>.testrail.io/'  # or other URL for self-hosted
login = '<account email>'
api_token = '<generated API token>'

client = TestRailClient(project_url, login, api_token)

created_run = client.runs.get_run(run_id=1)

"""
API response looks like:

{
    ...
    'refs': 'SAN-1',
    'custom_status1_count': 0,
    'custom_status2_count': 0,
    'custom_status3_count': 0,
    'custom_status4_count': 0,
    'custom_status5_count': 0,
    'custom_status6_count': 0,
    'custom_status7_count': 0,
    'description': null,
    ...
}

It is now stored in custom attribute:
created_run.custom == {
    'custom_status1_count': 0,
    'custom_status2_count': 0,
    'custom_status3_count': 0,
    'custom_status4_count': 0,
    'custom_status5_count': 0,
    'custom_status6_count': 0,
    'custom_status7_count': 0,
}
"""
```

## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have.
   Wait for approve from maintainer.
1. Create a pull request. Make sure all checks are green.
1. Fix review comments if any.
1. Be awesome.

Here are useful tips:

- You can run all checks and tests with `make check`.
  Please do it before TravisCI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.
