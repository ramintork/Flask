import pytest
import sys
import json

from jobs import app
from .utils import *


@pytest.mark.test_review_template_module7
def test_review_template_module7():
    review_exists = template_exists("review")
    assert (
        review_exists
    ), "The `review.html` template does not exist in the `templates` folder."

    el = template_data("review").select(".field.is-grouped .control .button.is-text")
    el_len = len(el) == 1
    assert (
        el_len
    ), "Has the `HTML` from `templates.html` been copied to the `review.html` template?"

    review_extends = "layout.html" in template_extends("review")
    assert review_extends, "The `review.html` template does not extend `layout.html`."

    review_url_for = "employer:employer_id:employer_id" in template_functions(
        "review", "url_for"
    )
    assert (
        review_url_for
    ), "Have you called the `url_for` function in the `review.html` file?"


@pytest.mark.test_app_review_route_module7
def test_app_review_route_module7():
    review_function = "review" in dir(app)
    assert review_function, "Have you created the `review` function?"

    employer_id = "employer_id" in inspect.getfullargspec(app.review).args
    assert (
        employer_id
    ), "Have you added the correct parameters to the `review` function parameter list?"

    route_pattern = (
        "route:/employer/<employer_id>/review:methods:[{'s': 'GET'}, {'s': 'POST'}]"
        or "route:/employer/<employer_id>/review:methods:[{'s': 'POST'}, {'s': 'GET'}]"
        in get_functions(app.review)
    )
    assert (
        route_pattern
    ), "Do you have a route decorator with the correct URL pattern and methods?"

    result = [
        item
        for item in get_functions(app.review)
        if item.startswith("render_template:review.html:employer_id:employer_id")
    ]
    result_len = len(result) == 1
    assert (
        result_len
    ), "Have you called the `render_template` function with the correct arguments."

    return_values = get_functions_returns(app.review)
    employer = {
        "value/args/args/s": "employer",
        "value/args/func/id": "url_for",
        "value/args/keywords/arg": "employer_id",
        "value/args/keywords/value/id": "employer_id",
        "value/func/id": "redirect",
    }
    render = {
        "value/args/s": "review.html",
        "value/func/id": "render_template",
        "value/keywords/arg": "employer_id",
        "value/keywords/value/id": "employer_id",
    }

    render_return = render in return_values
    assert render_return, "Did you return the `render_template` call?"

    employer_return = employer in return_values
    assert employer_return, "Did you return a call to `redirect` and `url_for`?"


@pytest.mark.test_app_review_post_request_check_module7
def test_app_review_post_request_check_module7():
    review_function = "review" in dir(app)
    assert review_function, "Have you created the `review` function?"

    datetime_exists = "datetime" in dir(app)
    assert datetime_exists, "`datetime` has not been imported."

    if_statement = get_statements(app.review)[0]
    body = if_statement["body"]
    for item in body:
        item.pop("type_comment", None)
        item.pop("value/slice/value/value", None)
        item.pop("value/args/value", None)

    post = (
        "test/comparators/s" in if_statement
        and "POST" == if_statement["test/comparators/s"]
    )
    method = (
        "test/left/attr" in if_statement and "method" == if_statement["test/left/attr"]
    )
    request = (
        "test/left/value/id" in if_statement
        and "request" == if_statement["test/left/value/id"]
    )
    eq = (
        "test/ops/node_type" in if_statement
        and "Eq" == if_statement["test/ops/node_type"]
    )
    review = {
        "targets/id": "review",
        "value/slice/value/s": "review",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    rating = {
        "targets/id": "rating",
        "value/slice/value/s": "rating",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    title = {
        "targets/id": "title",
        "value/slice/value/s": "title",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    status = {
        "targets/id": "status",
        "value/slice/value/s": "status",
        "value/value/attr": "form",
        "value/value/value/id": "request",
    }
    date = {
        "targets/id": "date",
        "value/args/s": "%m/%d/%Y",
        "value/func/attr": "strftime",
        "value/func/value/func/attr": "now",
        "value/func/value/func/value/attr": "datetime",
        "value/func/value/func/value/value/id": "datetime",
    }

    post_if = post and method and request and eq
    assert (
        post_if
    ), 'Do you have an `if` statement to test if the request method equals "POST?'

    body_review = review in body
    assert body_review, "Have you created the `review` variable?"

    body_rating = rating in body
    assert body_rating, "Have you created the `rating` variable?"

    body_title = title in body
    assert body_title, "Have you created the `title` variable?"

    body_status = status in body
    assert body_status, "Have you created the `status` variable?"

    body_date = date in body
    assert body_date, "Have you created the `date` variable?"


@pytest.mark.test_app_review_insert_review_module7
def test_app_review_insert_review_module7():
    review_function = "review" in dir(app)
    assert review_function, "Have you created the `review` function?"

    execute_sql = "execute_sql:INSERT INTO review (review, rating, title, date, status, employer_id) VALUES (?, ?, ?, ?, ?, ?):[{'id': 'review'}, {'id': 'rating'}, {'id': 'title'}, {'id': 'date'}, {'id': 'status'}, {'id': 'employer_id'}]:commit:True"
    result = [
        item for item in get_functions(app.review) if item.startswith(execute_sql)
    ]
    result_len = len(result) == 1
    assert result_len, "`execute_sql` has not been called or has the wrong parameters."


@pytest.mark.test_app_redirect_to_employer_module7
def test_app_redirect_to_employer_module7():
    review_function = "review" in dir(app)
    assert review_function, "Have you created the `review` function?"

    redirect_exists = "redirect" in dir(app)
    assert redirect_exists, "`redirect` has not been imported from flask."

    url_for_exists = "url_for" in dir(app)
    assert url_for_exists, "`url_for` has not been imported from flask."

    redirect_call = "redirect:employer:url_for:employer_id:employer_id" in get_functions(
        app.review
    ) or "redirect:employer:employer:url_for:employer_id:employer_id" in get_functions(
        app.review
    )
    assert redirect_call, "In the `if` are you redirecting back to the employer page?"


@pytest.mark.test_employer_review_button_module7
def test_employer_review_button_module7():
    employer_exists = template_exists("employer")
    assert (
        employer_exists
    ), "The `employer.html` template does not exist in the `templates` folder."

    review_button = "review:employer_id:employer:id" in template_functions(
        "employer", "url_for"
    )
    assert review_button, "Does the `Create Review` button have the correct `href`?"
