import os
import time
import pytest
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
    """Start the Flask app in a background thread for E2E tests."""
    port = int(os.environ.get('TEST_PORT', '5010'))
    srv = ServerThread(flask_app, port=port)
    srv.start()
    # wait briefly for server to start
    time.sleep(0.5)
    yield f'http://127.0.0.1:{port}'
    srv.shutdown()
