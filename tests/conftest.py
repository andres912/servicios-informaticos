from project import create_app, db
import pytest

@pytest.fixture(scope="function")
def test_client():
    flask_app = create_app("../instance/flask_test.cfg")
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope="function")
def init_database(test_client):
    db.create_all()

    yield db  # this is where the testing happens!

    db.session.remove()
    db.drop_all()
