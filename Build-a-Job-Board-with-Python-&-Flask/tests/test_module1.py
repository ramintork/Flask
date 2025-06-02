import pytest
import inspect

from .utils import *
from jobs import app


@pytest.mark.test_app_import_flask_module1
def test_app_import_flask_module1():
    flask_exists = "Flask" in dir(app)
    assert flask_exists, "Have you imported the `Flask` class from `flask`?"

    flask_is_class = inspect.isclass(app.Flask)
    assert flask_is_class, "`Flask` is not a class."

    render_template_exists = "render_template" in dir(app)
    assert render_template_exists, "`render_template` has not been imported."

    render_template_is_function = inspect.isfunction(app.render_template)
    assert render_template_is_function, "`render_template` is not a function."


@pytest.mark.test_app_create_flask_app_module1
def test_app_create_flask_app_module1():
    flask_app = "app" in dir(app)
    assert flask_app, "Have you created an instance of the `Flask` class called `app`?"

    flask_instance = isinstance(app.app, app.Flask)
    assert flask_instance, "`app` is not an instance of the `Flask` class."


@pytest.mark.test_index_template_module1
def test_index_template_module1():
    template_dir = os.path.isdir("jobs/templates")
    assert template_dir, "The `templates` folder has not been created."

    index_exists = template_exists("index")
    assert (
        index_exists
    ), "The `index.html` template does not exist in the `templates` folder."

    h1_exists = template_find("index", "h1", limit=1)
    assert (
        h1_exists
    ), "The `<h1>` in the `index.html` template does not contain the contents 'Jobs'."

    h1_jobs = template_find("index", "h1", limit=1)[0].text == "Jobs"
    assert (
        h1_jobs
    ), "The `<h1>` in the `index.html` template does not contain the contents 'Jobs'."


@pytest.mark.test_app_index_route_function_module1
def test_app_index_route_function_module1():
    flask_app = "app" in dir(app)
    assert flask_app, "Have you created an instance of the `Flask` class called `app`?"

    jobs_function = "jobs" in dir(app)
    assert jobs_function, "Have you created the `jobs` function?"

    result = [
        item
        for item in get_functions(app.jobs)
        if item.startswith("render_template:index.html")
    ]
    result_len = len(result) == 1
    assert result_len, "Have you called the `render_template` function."

    return_values = get_functions_returns(app.jobs)[0]
    return_exists = (
        return_values["value/args/s"] == "index.html"
        and return_values["value/func/id"] == "render_template"
    )
    assert return_exists, "Did you return the `render_template` call?"


@pytest.mark.test_app_route_decoractors_module1
def test_app_route_decoractors_module1():
    flask_app = "app" in dir(app)
    assert flask_app, "Have you created an instance of the `Flask` class called `app`?"

    index_exists = template_exists("index")
    assert (
        index_exists
    ), "The `index.html` template does not exist in the `templates` folder."

    jobs_function = "jobs" in dir(app)
    assert jobs_function, "Have you created the `jobs` function?"

    rules = list_routes(app.app)
    root_route = "jobs:GET,HEAD,OPTIONS:/" in rules
    assert root_route, "Have you decorated the `jobs` function with the `/` route?"

    jobs_route = "jobs:GET,HEAD,OPTIONS:/jobs" in rules
    assert jobs_route, "Have you decorated the `jobs` function with the `/jobs` route?"
