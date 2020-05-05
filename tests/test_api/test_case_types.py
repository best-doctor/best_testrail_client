def test_get_case_types(testrail_client, mocked_response, case_types_data, case_types):
    mocked_response(data_json=[case_types_data])

    api_case_types = testrail_client.get_case_types()

    assert len(api_case_types) == 1
    assert api_case_types[0] == case_types
