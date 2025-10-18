import requests
from behave import then, when

API_BASE_URL = "http://127.0.0.1:5000"


@when('I request "/raise500"')
def when_request_raise500(context):
    context.response = requests.get(f"{API_BASE_URL}/raise500")


@then("the response code should be 500")
def then_response_code_500(context):
    assert context.response.status_code == 500


@then('the response should contain "Internal server error"')
def then_response_contains_internal_server_error(context):
    assert "Internal server error" in context.response.text


@then("the error response should not contain exception details")
def then_error_response_should_not_contain_exception_details(context):
    assert "Exception" not in context.response.text
    assert "Traceback" not in context.response.text


@when('I request "/raise_exception"')
def when_request_raise_exception(context):
    context.response = requests.get(f"{API_BASE_URL}/raise_exception")


@then('the response should contain "Unexpected server error"')
def then_response_contains_unexpected_server_error(context):
    assert "Unexpected server error" in context.response.text
