from webapp.models.Shortcode import Shortcode
from http import HTTPStatus
import json


def test_shorten_missing_body(app):
    """Ensures 400 HTTP code when missing request body"""

    with app.test_client() as client:
        response = client.post(
            '/shorten',
            content_type='application/json',
        )
        data = response.data.decode()
        print(response.data)
        assert response.status_code == HTTPStatus.BAD_REQUEST

def test_shorten_missing_url_body_attribute(app):
    """Ensures 400 HTTP code when missing 'url' request body attribute"""

    with app.test_client() as client:
        response = client.post(
            '/shorten',
            data=json.dumps(dict()),
            content_type='application/json',
        )
        data = response.data.decode()
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert 'Url not present' in data

def test_shorten_invalid_shortcode_body_attribute(app):
    """Ensures 412 HTTP code when invalid 'shortcode' request body attribute"""

    with app.test_client() as client:
        response = client.post(
            '/shorten',
            data=json.dumps(dict(
                url='https://www.energyworx.com/',
                shortcode='ewx%'
            )),
            content_type='application/json',
        )
        data = response.data.decode()
        assert response.status_code == HTTPStatus.PRECONDITION_FAILED
        assert 'The provided shortcode is invalid' in data

def test_shorten_valid_shortcode_body_attribute(app):
    """Ensures 200 HTTP code when valid and not assigned 'shortcode' request body attribute"""

    with app.test_client() as client:
        size = len(Shortcode.query.all())
        response = client.post(
            '/shorten',
            data=json.dumps(dict(
                url='https://www.energyworx.com/',
                shortcode='ewx123'
            )),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        created = Shortcode.query.get(data['created_id'])
        assert response.status_code == HTTPStatus.OK
        assert created
        assert size + 1 == len(Shortcode.query.all())
        assert created.created
        assert not created.last_redirect
        assert created.redirect_count == 0

def test_shorten_assigned_shortcode_body_attribute(app):
    """Ensures 409 HTTP code when assigned 'shortcode' request body attribute"""

    with app.test_client() as client:
        response = client.post(
            '/shorten',
            data=json.dumps(dict(
                url='https://www.energyworx.com/',
                shortcode='ewx123'
            )),
            content_type='application/json',
        )
        data = response.data.decode()
        assert response.status_code == HTTPStatus.CONFLICT
        assert 'Shortcode already in use' in data

def test_shorten_missing_shortcode_body_attribute(app):
    """Ensures 200 HTTP code when missing 'shortcode' request body attribute"""

    with app.test_client() as client:
        size = len(Shortcode.query.all())
        response = client.post(
            '/shorten',
            data=json.dumps(dict(
                url='https://www.energyworx.com/'
            )),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        created = Shortcode.query.get(data['created_id'])
        assert response.status_code == HTTPStatus.OK
        assert created
        assert Shortcode.is_valid(Shortcode.query.get(data['created_id']).shortcode)
        assert size + 1 == len(Shortcode.query.all())
        assert created.created
        assert not created.last_redirect
        assert created.redirect_count == 0


def test_shortcode_not_found(app):
    """Ensures 404 HTTP code when non existing :shortcode"""

    with app.test_client() as client:
        response = client.get('/ewx404')
        data = response.data.decode()
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert 'Shortcode not found' in data

def test_shortcode_found(app):
    """
    Ensures 302 HTTP code when existing :shortcode
    Ensures 'redirect_count' is incremented and 'last_redirect' updated
    """

    with app.test_client() as client:
        before_redirect_count = Shortcode.query.filter_by(shortcode='ewx123').one().redirect_count
        response = client.get('/ewx123')
        after = Shortcode.query.filter_by(shortcode='ewx123').one()
        assert response.status_code == HTTPStatus.FOUND
        assert after.redirect_count == before_redirect_count + 1
        assert after.last_redirect


def test_shortcode_stats_not_found(app):
    """Ensures 404 HTTP code when non existing :shortcode"""

    with app.test_client() as client:
        response = client.get('/ewx404/stats')
        data = response.data.decode()
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert 'Shortcode not found' in data

def test_shortcode_stats_found(app):
    """Ensures 200 HTTP code when existing :shortcode"""

    with app.test_client() as client:
        response = client.get('/ewx123/stats')
        assert response.status_code == HTTPStatus.OK
