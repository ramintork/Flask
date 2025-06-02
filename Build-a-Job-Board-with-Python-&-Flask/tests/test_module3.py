import pytest
import inspect

from jobs import app
from .utils import *


@pytest.mark.test_app_import_sqlite_module3
def test_app_import_sqlite_module3():
    sqlite_import = "sqlite3" in dir(app)
    assert sqlite_import, "Have you imported `sqlite`?"


@pytest.mark.test_app_import_g_module3
def test_app_import_g_module3():
    g_import = "g" in dir(app)
    assert g_import, "Have you imported the `g` class from `flask`?"


@pytest.mark.test_app_db_path_module3
def test_app_db_path_module3():
    assert "PATH" in dir(app), "Have you created a constant called `PATH`?"
    assert app.PATH == "db/jobs.sqlite", "Have you created a constant called `PATH`?"


@pytest.mark.test_app_open_connection_get_attribute_module3
def test_app_open_connection_get_attribute_module3():

    open_connection = "open_connection" in dir(app)
    assert open_connection, "Have you defined a function named `open_connection`?"

    result = [
        item
        for item in get_functions(app.open_connection)
        if item.startswith("getattr:g:_connection")
    ]
    result_len = len(result) == 1
    assert (
        result_len
    ), "Have you used the `getattr` function to get the global `_connection`?"


@pytest.mark.test_app_open_connection_connection_module3
def test_app_open_connection_connection_module3():
    g_import = "g" in dir(app)
    assert g_import, "Have you imported the `g` class from `flask`?"

    flask_app = "app" in dir(app)
    assert flask_app, "Have you created an instance of the `Flask` class called `app`?"

    open_connection = "open_connection" in dir(app)
    assert open_connection, "Have you defined a function named `open_connection`?"

    with app.app.app_context():
        app.open_connection()

        connection_exists = hasattr(app.g, "_connection")
        assert connection_exists, "Did you assign the `_connection` attribute to `g`?"

        _, _, db_name = app.g._connection.execute("PRAGMA database_list").fetchone()
        db_exists = os.path.join(os.getcwd(), "db", "jobs.sqlite") == db_name
        assert db_exists, "Did you pass the `connect` function the `PATH` constant?"


@pytest.mark.test_app_open_connection_row_factory_module3
def test_app_open_connection_row_factory_module3():
    g_import = "g" in dir(app)
    assert g_import, "Have you imported the `g` class from `flask`?"

    flask_app = "app" in dir(app)
    assert flask_app, "Have you created an instance of the `Flask` class called `app`?"

    open_connection = "open_connection" in dir(app)
    assert open_connection, "Have you defined a function named `open_connection`?"

    with app.app.app_context():
        db = app.open_connection()
        return_connection = isinstance(db, app.sqlite3.Connection)
        assert return_connection, "Are you returning the database connection?"

        row_factory = id(db.row_factory) == id(app.sqlite3.Row)
        assert (
            row_factory
        ), "Have you set the database `row_factory` to the sqlite3.Row class?"


@pytest.mark.test_app_execute_sql_module3
def test_app_execute_sql_module3():
    flask_app = "app" in dir(app)
    assert flask_app, "Have you created an instance of the `Flask` class called `app`?"

    execute_sql_function = "execute_sql" in dir(app)
    assert execute_sql_function, "Have you defined a function named `execute_sql`?"

    open_call = "open_connection" in get_functions(app.execute_sql)
    assert open_call, "Have you called the `open_connection` function in `execute_sql`?"


@pytest.mark.test_app_execute_sql_parameters_module3
def test_app_execute_sql_parameters_module3():
    execute_sql_function = "execute_sql" in dir(app)
    assert execute_sql_function, "Have you defined a function named `execute_sql`?"

    parameters = inspect.getfullargspec(app.execute_sql)
    arg_len = len(parameters.args) == 4
    assert arg_len, "Have you added parameters to the `execute_sql` function?"

    args = (
        parameters.args[0] == "sql"
        and parameters.args[1] == "values"
        and parameters.args[2] == "commit"
        and parameters.args[3] == "single"
    )
    assert (
        args
    ), "Have you added the correct parameters to the `execute_sql` function parameters list?"

    defaults = (
        parameters.defaults[0] == ()
        and parameters.defaults[1] == False
        and parameters.defaults[2] == False
    )
    assert (
        defaults
    ), "Do the `args` and `one` parameters have the correct defaults in the `execute_sql` function parameters list?"


@pytest.mark.test_app_execute_sql_execute_module3
def test_app_execute_sql_execute_module3():
    execute_sql_function = "execute_sql" in dir(app)
    assert execute_sql_function, "Have you defined a function named `execute_sql`?"

    execute_call = "execute:sql:values" in get_functions(app.execute_sql)
    assert execute_call, "Have you called the `execute` function in `execute_sql`?"


@pytest.mark.test_app_execute_sql_results_module3
def test_app_execute_sql_results_module3():
    execute_sql_function = "execute_sql" in dir(app)
    assert execute_sql_function, "Have you defined a function named `execute_sql`?"

    fetchall = "fetchall" in get_functions(app.execute_sql)
    assert fetchall, "Have you called the `fetchall` function in `execute_sql`?"

    fetchone = "fetchone" in get_functions(app.execute_sql)
    assert fetchone, "Have you called the `fetchone` function in `execute_sql`?"

    commit = "commit" in get_functions(app.execute_sql)
    assert commit, "Have you called the `commit` function in `execute_sql`?"

    close = "close" in get_functions(app.execute_sql)
    assert close, "Have you called the `close` function in `execute_sql`?"

    if_statement = len(get_statements(app.execute_sql)) >= 0
    assert if_statement, "Have created an if statement in the `execute_sql` function?"

    results_exists = "results" == get_statements(app.execute_sql)[0]["body/targets/id"]
    assert (
        results_exists
    ), "Have you assigned the `results` variable to `connection.commit()`?"

    with app.app.app_context():
        results = type(app.execute_sql("SELECT * FROM job", single=True)) != list
        assert (
            results
        ), "Have you create an if statement to only return one result in `one` is true?"


@pytest.mark.test_app_close_connection_module3
def test_app_close_connection_module3():
    close_connection = "close_connection" in dir(app)
    assert close_connection, "Have you defined a function named `close_connection`?"

    result = [
        item
        for item in get_functions(app.open_connection)
        if item.startswith("getattr:g:_connection")
    ]
    result_len = len(result) == 1
    assert (
        result_len
    ), "Have you used the `getattr` function to get the global `_connection`?"

    close = "close" in get_functions(app.close_connection)
    assert close, "Have you called the `close` function in `close_connection`?"


@pytest.mark.test_app_close_connection_decorator_module3
def test_app_close_connection_decorator_module3():
    close_connection = "close_connection" in dir(app)
    assert close_connection, "Have you defined a function named `close_connection`?"

    decorators = get_decorators(app.close_connection)["close_connection"]

    decorators_len = len(decorators) == 1
    assert decorators_len, "Have you added the correct decorator to `close_connection`?"

    decorator = decorators[0][0]
    teardown = decorator == "teardown_appcontext"
    assert teardown, "Does `close_connection` have a `teardown_appcontext` decorator?"
