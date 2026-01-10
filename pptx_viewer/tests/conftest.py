import os
import time
import pytest
import urllib.request
from threading import Thread
from werkzeug.serving import make_server

from app import app as flask_app


class ServerThread(Thread):
    def __init__(self, app, host='127.0.0.1', port=5010):
        super().__init__(daemon=True)
        self.srv = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()
        self.port = port

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


@pytest.fixture(scope='session')
def live_server():
    """Start the Flask app in a background thread for E2E tests.

    This fixture now polls the server URL until it responds with HTTP 200 or a
    timeout is reached. A short fixed sleep was flaky on CI/ubuntu runners.
    """
    port = int(os.environ.get('TEST_PORT', '5010'))
    srv = ServerThread(flask_app, port=port)
    srv.start()

    # wait for server to be ready by polling the root URL
    url = f'http://127.0.0.1:{port}/'
    timeout = 10  # seconds
    start = time.time()
    while True:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    break
        except Exception:
            if time.time() - start > timeout:
                srv.shutdown()
                pytest.fail(f'Live server failed to start on {url} within {timeout}s')
            time.sleep(0.5)

    yield f'http://127.0.0.1:{port}'
    srv.shutdown()
