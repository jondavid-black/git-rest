import os
import time
from multiprocessing import Process

import pytest
from playwright.sync_api import sync_playwright
from werkzeug.serving import make_server

from git_rest.app import create_app


@pytest.fixture(scope="module")
def flask_app_server():
    os.environ["GIT_REST_UI"] = "1"
    app = create_app()
    server = make_server("127.0.0.1", 5005, app)
    proc = Process(target=server.serve_forever)
    proc.start()
    time.sleep(1)  # Give server time to start
    yield
    proc.terminate()
    proc.join()


def test_apidocs_descriptions_and_fallback(flask_app_server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:5005/apidocs/")
        # Wait for the endpoint description to appear in the DOM
        description = (
            "List all files and directories in the specified repository for a user."
        )
        try:
            page.wait_for_function(
                f"document.body.innerText.includes('{description}')", timeout=15000
            )
            found = True
        except Exception:
            found = False
            print(page.content())
        assert found, f"Endpoint description '{description}' not found in Swagger UI."
        browser.close()
