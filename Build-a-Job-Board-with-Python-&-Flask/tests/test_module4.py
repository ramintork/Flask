import pytest
import sys

from jobs import app
from .utils import *


@pytest.mark.test_template_macros_module4
def test_template_macros_module4():
    macros_exists = template_exists("_macros")
    assert (
        macros_exists
    ), "The `_macros.html` template does not exist in the `templates` folder."


@pytest.mark.test_show_job_macro_definition_module4
def test_show_job_macro_definition_module4():
    macros_exists = template_exists("_macros")
    assert (
        macros_exists
    ), "The `_macros.html` template does not exist in the `templates` folder."

    show_job = "show_job:job" in template_macros("_macros")
    assert (
        show_job
    ), "Have you created the `show_job` macro and added the correct parameter?"


@pytest.mark.test_show_job_macro_html_module4
def test_show_job_macro_html_module4():
    macros_exists = template_exists("_macros")
    assert (
        macros_exists
    ), "The `_macros.html` template does not exist in the `templates` folder."

    html = template_macro_soup("_macros", "show_job")
    p = html.select(".card .card-header .card-header-title")
    div = html.select(".card-content .content")

    copied = len(p) == 1 and len(div) == 1
    assert (
        copied
    ), "Has the `HTML` from `templates.html` been copied to the `show_job` macro?"


@pytest.mark.test_show_job_macro_header_module4
def test_show_job_macro_header_module4():
    macros_exists = template_exists("_macros")
    assert (
        macros_exists
    ), "The `_macros.html` template does not exist in the `templates` folder."

    job_title = "job:title" in template_variables("_macros")
    assert job_title, "Looks like the job title link does not have content."


@pytest.mark.test_show_job_macro_body_module4
def test_show_job_macro_body_module4():
    macros_exists = template_exists("_macros")
    assert (
        macros_exists
    ), "The `_macros.html` template does not exist in the `templates` folder."

    employer_name = "job:employer_name" in template_variables("_macros")
    assert employer_name, "Are you showing the employer name?"

    salary = "job:salary" in template_variables("_macros")
    assert salary, "Are you showing the job salary?"

    description = "job:description" in template_variables("_macros")
    assert description, "Are you showing the job description?"


@pytest.mark.test_show_jobs_macro_definition_module4
def test_show_jobs_macro_definition_module4():
    macros_exists = template_exists("_macros")
    assert (
        macros_exists
    ), "The `_macros.html` template does not exist in the `templates` folder."

    show_jobs = "show_jobs:jobs" in template_macros("_macros")
    assert (
        show_jobs
    ), "Have you created the `show_jobs` macro and added the correct parameter?"


@pytest.mark.test_show_jobs_macro_for_loop_module4
def test_show_jobs_macro_for_loop_module4():
    macros_exists = template_exists("_macros")
    assert (
        macros_exists
    ), "The `_macros.html` template does not exist in the `templates` folder."

    show_jobs = "show_jobs:jobs" in template_macros("_macros")
    assert (
        show_jobs
    ), "Have you created the `show_jobs` macro and added the correct parameter?"

    div = template_macro_soup("_macros", "show_jobs").select("div.columns.is-multiline")
    div_len = len(div) == 1
    assert (
        div_len
    ), "Has a `<div>` with classes of `columns` and `is-multiline` been added to the `show_jobs` macro?"

    show_job_for = "job:jobs" in show_jobs_for()
    assert show_job_for, "Does the `show_jobs` macro contain a `for` loop?"


@pytest.mark.test_show_jobs_macro_for_loop_body_module4
def test_show_jobs_macro_for_loop_body_module4():
    macros_exists = template_exists("_macros")
    assert (
        macros_exists
    ), "The `_macros.html` template does not exist in the `templates` folder."

    show_jobs = "show_jobs:jobs" in template_macros("_macros")
    assert (
        show_jobs
    ), "Have you created the `show_jobs` macro and added the correct parameter?"

    div = template_macro_soup("_macros", "show_jobs").select("div.column.is-half")
    div_len = len(div) == 1
    assert (
        div_len
    ), "Has a `<div>` with classes of `column` and `is-half` been added to the `show_jobs` macro `for` loop body?"

    show_job_call = "show_job:job" in show_jobs_for()
    assert show_job_call, "Does the `show_jobs` macro call `show_job`?"


@pytest.mark.test_import_macros_module4
def test_import_macros_module4():
    macros_exists = template_exists("_macros")
    assert (
        macros_exists
    ), "The `_macros.html` template does not exist in the `templates` folder."

    import_exists = "_macros.html:show_job:show_jobs:True" == template_import("layout")
    assert import_exists, "Have you imported `_macros.html` in `layout.html`?"


@pytest.mark.test_index_template_module4
def test_index_template_module4():
    index_exists = template_exists("index")
    assert (
        index_exists
    ), "The `index.html` template does not exist in the `templates` folder."

    el = len(template_data("index").select(".columns .column.is-one-fifth")) == 1
    assert (
        el
    ), "Has the `HTML` from `templates.html` been copied to the `index.html` template?"


@pytest.mark.test_display_all_jobs_module4
def test_display_all_jobs_module4():
    index_exists = template_exists("index")
    assert (
        index_exists
    ), "The `index.html` template does not exist in the `templates` folder."

    show_jobs_call = "show_jobs:jobs" in template_functions("index", "show_jobs")
    assert (
        show_jobs_call
    ), "Have you call the `show_jobs` macro in the `index.html` file?"


@pytest.mark.test_app_jobs_route_jobs_module4
def test_app_jobs_route_jobs_module4():
    jobs_function = "jobs" in dir(app)
    assert jobs_function, "Have you created the `jobs` function?"

    execute_sql = "execute_sql:SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id"
    sql_exists = execute_sql in get_functions(app.jobs)
    assert sql_exists, "`execute_sql` has not been called or has the wrong parameters."

    new_render_call = "render_template:index.html:jobs:jobs" in get_functions(app.jobs)
    assert new_render_call, "Have you added `jobs` to the `render_template` call."
