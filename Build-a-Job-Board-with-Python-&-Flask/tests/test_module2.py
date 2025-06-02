import pytest

from jobs import app
from .utils import *

calls = template_functions("layout", "url_for")


@pytest.mark.test_layout_template_module2
def test_layout_template_module2():
    layout_exists = template_exists("layout")
    assert (
        layout_exists
    ), "The `layout.html` template does not exist in the `templates` folder."


@pytest.mark.test_add_bulma_css_framework_module2
def test_add_bulma_css_framework_module2():
    layout_exists = template_exists("layout")
    assert (
        layout_exists
    ), "The `layout.html` template does not exist in the `templates` folder."

    css_exists = "static:filename:css/bulma.min.css" in calls
    assert css_exists, "Looks like `bulma.min.css` is not linked in `layout.html`."


@pytest.mark.test_add_custom_css_module2
def test_add_custom_css_module2():
    layout_exists = template_exists("layout")
    assert (
        layout_exists
    ), "The `layout.html` template does not exist in the `templates` folder."

    css_exists = "static:filename:css/app.css" in calls
    assert css_exists, "Looks like `app.css` is not linked in `layout.html`."


@pytest.mark.test_add_fontawesome_module2
def test_add_fontawesome_module2():
    layout_exists = template_exists("layout")
    assert (
        layout_exists
    ), "The `layout.html` template does not exist in the `templates` folder."

    attr = {
        "href": "https://use.fontawesome.com/releases/v5.2.0/css/all.css",
        "rel": "stylesheet",
    }
    layout_link_exists = template_soup("layout").find("link", attr)
    assert layout_link_exists, "Looks like FontAwesome is not linked in `layout.html`."


@pytest.mark.test_extend_base_template_module2
def test_extend_base_template_module2():
    index_exists = template_exists("index")
    assert (
        index_exists
    ), "The `index.html` template does not exist in the `templates` folder."

    layout_exists = template_exists("layout")
    assert (
        layout_exists
    ), "The `layout.html` template does not exist in the `templates` folder."

    index_extends = "layout.html" in template_extends("index")
    assert index_extends, "The `index.html` template does not extend `layout.html`."

    content_block = "content" in template_block("index")
    assert content_block, "Have you added a template `block` called `content`?"
