from webapp import create_app, db
import pytest


@pytest.fixture(scope="session")
def app():
    test_app = create_app(env='testing')

    with test_app.app_context():
        db.create_all()

        yield test_app

        db.session.remove()
        db.drop_all()
