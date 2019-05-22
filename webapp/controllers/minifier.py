from flask import Blueprint, abort, request
from webapp import db
from webapp.models.Shortcode import Shortcode
from http import HTTPStatus

minifier = Blueprint('minifier', __name__)


@minifier.route('/shorten', methods=['POST'])
def shorten_route():

    data = request.json

    # Raise 400 if body not defined or 'url' not present
    if not data or not data.get('url'):
        abort(HTTPStatus.BAD_REQUEST, 'Url not present')

    if data.get('shortcode'):

        # Raise 412 if shortcode is not valid
        if not Shortcode.valid(data['shortcode']):
            abort(HTTPStatus.PRECONDITION_FAILED, 'The provided shortcode is invalid')

        shortcode = Shortcode.query.filter_by(shortcode=data['shortcode']).first()

        # Raise 409 if shortcode already in use
        if shortcode:
            abort(HTTPStatus.CONFLICT, 'Shortcode already in use')

        # Adding new shortcode entry with data provided
        shortcode = Shortcode(url=data['url'], shortcode=data['shortcode'])
        db.session.add(shortcode)
        db.session.commit()

    else:
        shortcode = Shortcode(url=data['url'], shortcode=Shortcode.generate_code())
        db.session.add(shortcode)
        db.session.commit()

    return 'Success'
