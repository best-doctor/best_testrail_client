def test_get_result_fields(testrail_client, mocked_response, result_fields_data, result_fields):
    mocked_response(data_json=[result_fields_data])

    api_result_fields = testrail_client.get_result_fields()

    assert len(api_result_fields) == 1
    assert api_result_fields[0] == result_fields
