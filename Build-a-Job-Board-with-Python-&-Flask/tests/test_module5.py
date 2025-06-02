import pytest
import sys

from jobs import app
from .utils import *


@pytest.mark.test_app_job_template_module5
def test_app_job_template_module5():

    job_exists = template_exists("job")
    assert (
        job_exists
    ), "The `job.html` template does not exist in the `templates` folder."

    job_extends = "layout.html" in template_extends("job")
    assert job_extends, "The `job.html` template does not extend `layout.html`."

    content_block = "content" in template_block("job")
    assert content_block, "Have you added a template `block` called `content`?"

    show_job = "show_job:job" in template_functions("job", "show_job")
    assert show_job, "Have you call the `show_job` macro in the `job.html` file?"


@pytest.mark.test_app_job_route_module5
def test_app_job_route_module5():
    jobs_function = "jobs" in dir(app)
    assert jobs_function, "Have you created the `jobs` function?"

    result = [
        item
        for item in get_functions(app.job)
        if item.startswith("render_template:job.html")
    ]
    result_len = len(result) == 1
    assert result_len, "Have you called the `render_template` function."

    return_values = get_functions_returns(app.job)[0]
    return_exists = (
        return_values["value/args/s"] == "job.html"
        and return_values["value/func/id"] == "render_template"
    )
    assert return_exists, "Did you return the `render_template` call?"


@pytest.mark.test_app_job_route_decorator_module5
def test_app_job_route_decorator_module5():
    jobs_function = "jobs" in dir(app)
    assert jobs_function, "Have you created the `jobs` function?"

    job_id = "route:/job/<job_id>" in get_functions(app.job)
    assert job_id, "Have you added a `job_id` parameter to the job function"


@pytest.mark.test_app_job_route_parameter_module5
def test_app_job_route_parameter_module5():
    jobs_function = "jobs" in dir(app)
    assert jobs_function, "Have you created the `jobs` function?"

    job_href = "job:job_id:job:id" in template_functions("_macros", "url_for")
    assert job_href, "Looks like the job title link `href` is incorrect."

    job_id = "job_id" in inspect.getfullargspec(app.job).args
    assert (
        job_id
    ), "Have you added the correct parameters to the `job` function parameters list?"


@pytest.mark.test_app_job_route_data_module5
def test_app_job_route_data_module5():
    jobs_function = "jobs" in dir(app)
    assert jobs_function, "Have you created the `jobs` function?"

    execute_sql = "execute_sql:SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?:job_id:single:True"
    result = [item for item in get_functions(app.job) if item.startswith(execute_sql)]
    result_len = len(result) == 1
    assert result_len, "`execute_sql` has not been called or has the wrong parameters."


@pytest.mark.test_app_job_route_pass_data_module5
def test_app_job_route_pass_data_module5():
    jobs_function = "jobs" in dir(app)
    assert jobs_function, "Have you created the `jobs` function?"

    new_render = "render_template:job.html:job:job" in get_functions(app.job)
    assert new_render, "Have you added `job` to the `render_template` call."
