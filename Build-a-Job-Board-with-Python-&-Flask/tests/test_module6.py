import pytest
import sys

from jobs import app
from .utils import *


@pytest.mark.test_employer_template_module6
def test_employer_template_module6():
    employer_exists = template_exists("employer")
    assert (
        employer_exists
    ), "The `employer.html` template does not exist in the `templates` folder."

    el = (
        len(template_data("employer").select(".box .media .media-content .content"))
        == 1
    )
    assert (
        el
    ), "Has the `HTML` from `templates.html` been copied to the `employer.html` template?"

    employer_extends = "layout.html" in template_extends("employer")
    assert (
        employer_extends
    ), "The `employer.html` template does not extend `layout.html`."


@pytest.mark.test_employer_template_details_module6
def test_employer_template_details_module6():
    employer_exists = template_exists("employer")
    assert (
        employer_exists
    ), "The `employer.html` template does not exist in the `templates` folder."

    employer_name = "employer:name" in template_variables("employer")
    assert (
        employer_name
    ), "Looks like the `employer['name']` is not present in the template."

    employer_description = "employer:description" in template_variables("employer")
    assert (
        employer_description
    ), "Looks like the `employer['description']` is not present in the template."


@pytest.mark.test_employer_template_all_jobs_module6
def test_employer_template_all_jobs_module6():
    employer_exists = template_exists("employer")
    assert (
        employer_exists
    ), "The `employer.html` template does not exist in the `templates` folder."

    show_job = "show_jobs:jobs" in template_functions("employer", "show_jobs")
    assert (
        show_job
    ), "Have you called the `show_jobs` macro in the `employer.html` file?"


@pytest.mark.test_employer_template_reviews_module6
def test_employer_template_reviews_module6():
    employer_exists = template_exists("employer")
    assert (
        employer_exists
    ), "The `employer.html` template does not exist in the `templates` folder."

    reviews_for = "review:reviews" in employer_for()
    assert reviews_for, "Have you created a `for` loop that cycles through `reviews`?"


@pytest.mark.test_employer_template_review_stars_module6
def test_employer_template_review_stars_module6():
    employer_exists = template_exists("employer")
    assert (
        employer_exists
    ), "The `employer.html` template does not exist in the `templates` folder."

    review_range = "_:range:0:review:rating" in employer_for()
    assert review_range, "Have you created a `for` loop that cycles through `reviews`?"
    el = len(template_data("employer").select(".fa.fa-star.checked")) == 1
    assert el, "Has the star `<span>` been added to the `employer.html` template?"


@pytest.mark.test_employer_template_review_details_module6
def test_employer_template_review_details_module6():
    employer_exists = template_exists("employer")
    assert (
        employer_exists
    ), "The `employer.html` template does not exist in the `templates` folder."

    review_title = "review:title" in template_variables("employer")
    assert (
        review_title
    ), "Looks like the `review['title']` is not present in the template."

    review_status = "review:status" in template_variables("employer")
    assert (
        review_status
    ), "Looks like the `review['status']` is not present in the template."

    review_date = "review:date" in template_variables("employer")
    assert (
        review_date
    ), "Looks like the `review['date']` is not present in the template."

    review_review = "review:review" in template_variables("employer")
    assert (
        review_review
    ), "Looks like the `review['review']` is not present in the template."


@pytest.mark.test_app_employer_route_module6
def test_app_employer_route_module6():
    employer_function = "employer" in dir(app)
    assert employer_function, "Have you created the `employer` function?"

    employer_route = "route:/employer/<employer_id>" in get_functions(app.employer)
    assert employer_route, "Does `employer` function have the correct route?"

    result = [
        item
        for item in get_functions(app.employer)
        if item.startswith("render_template:employer.html")
    ]
    result_len = len(result) == 1
    assert result_len, "Have you called the `render_template` function."

    return_values = get_functions_returns(app.employer)[0]
    return_exists = (
        return_values["value/args/s"] == "employer.html"
        and return_values["value/func/id"] == "render_template"
    )
    assert return_exists, "Did you return the `render_template` call?"

    job_title = "employer:employer_id:job:employer_id" in template_functions(
        "_macros", "url_for"
    )
    assert (
        job_title
    ), "Looks like the job title link `href` is incorrect in `_macros.html."


@pytest.mark.test_app_employer_route_employers_module6
def test_app_employer_route_employers_module6():
    employer_function = "employer" in dir(app)
    assert employer_function, "Have you created the `employer` function?"

    args = "employer_id" in inspect.getfullargspec(app.employer).args
    assert (
        args
    ), "Have you added the correct parameters to the `employer` function parameter list?"

    execute_sql = (
        "execute_sql:SELECT * FROM employer WHERE id=?:employer_id:single:True"
    )
    execute_sql_alternate = (
        "execute_sql:SELECT * FROM employer WHERE id = ?:employer_id:single:True"
    )

    result_sql = [
        item for item in get_functions(app.employer) if item.startswith(execute_sql)
    ]
    result_sql_len = len(result_sql) == 1

    result_sql_alternate = [
        item
        for item in get_functions(app.employer)
        if item.startswith(execute_sql_alternate)
    ]
    result_sql_alternate_len = len(result_sql_alternate) == 1

    sql_exists = result_sql_len or result_sql_alternate_len
    assert sql_exists, "`execute_sql` has not been called or has the wrong parameters."

    result = [
        item
        for item in get_functions(app.employer)
        if item.startswith("render_template:employer.html:employer:employer")
    ]
    result_len = len(result) == 1
    assert result_len, "Have you added `employer` to the `render_template` call."


@pytest.mark.test_app_employer_route_jobs_module6
def test_app_employer_route_jobs_module6():
    employer_function = "employer" in dir(app)
    assert employer_function, "Have you created the `employer` function?"

    execute_sql = "execute_sql:SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?:employer_id"
    sql_exists = execute_sql in get_functions(app.employer)
    assert sql_exists, "`execute_sql` has not been called or has the wrong parameters."

    result = [
        item
        for item in get_functions(app.employer)
        if item.startswith("render_template:employer.html:employer:employer:jobs:jobs")
    ]
    result_len = len(result) == 1
    assert result_len, "Have you added `jobs` to the `render_template` call."


@pytest.mark.test_app_employer_route_reviews_module6
def test_app_employer_route_reviews_module6():
    employer_function = "employer" in dir(app)
    assert employer_function, "Have you created the `employer` function?"

    execute_sql = "execute_sql:SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?:employer_id"
    sql_exists = execute_sql in get_functions(app.employer)
    assert sql_exists, "`execute_sql` has not been called or has the wrong parameters."

    result = [
        item
        for item in get_functions(app.employer)
        if item.startswith(
            "render_template:employer.html:employer:employer:jobs:jobs:reviews:reviews"
        )
    ]
    result_len = len(result) == 1
    assert result_len, "Have you added `reviews` to the `render_template` call."
