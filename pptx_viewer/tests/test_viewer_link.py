import os
import re
import pytest
from app import app as flask_app


def test_open_reveal_link_present_and_script():
    client = flask_app.test_client()
    r = client.get('/')
    assert r.status_code == 200
    html = r.get_data(as_text=True)

    # link element exists
    assert 'id="open-reveal"' in html

    # JS that sets the href in index.html should be present
    assert 'openReveal.href = `/reveal?thumbs=${thumbs ?' in html


@pytest.mark.skipif(not os.environ.get('RUN_E2E'), reason='E2E tests disabled; set RUN_E2E=1 to enable')
def test_open_reveal_href_e2e(live_server):
    # Uses Playwright (must be installed with `playwright install`)
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        pytest.skip(f'Playwright not available: {e}')

    url = live_server + '/'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        # wait for open-reveal link to be populated by JS
        page.wait_for_selector('#open-reveal')
        href = page.eval_on_selector('#open-reveal', 'el => el.href')
        browser.close()

    # href should be a full URL ending with /reveal?thumbs=true or false
    m = re.search(r'/reveal\?thumbs=(true|false)$', href)
    assert m, f'Unexpected href: {href}'
