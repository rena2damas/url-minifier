from flask import Blueprint, abort, request, redirect
from webapp import db
from webapp.models.Shortcode import Shortcode
from http import HTTPStatus
import datetime
import json

minifier = Blueprint('minifier', __name__)


@minifier.route('/shorten', methods=['POST'])
def shorten_route():
    """
    Creates a new shortcode

    Expect:
        200 if missing or valid 'shortcode' body attribute
        400 if body not defined or missing body 'url' attribute
        409 if shortcode attribute already assigned
        412 if invalid 'shortcode' body attribute
    """

    # Raise 400 if body not defined
    if not request.data:
        abort(HTTPStatus.BAD_REQUEST)

    data = request.json

    # Raise 400 if 'url' not present
    if not data.get('url'):
        abort(HTTPStatus.BAD_REQUEST, 'Url not present')

    if data.get('shortcode'):

        # Raise 412 if shortcode is not valid
        if not Shortcode.is_valid(data['shortcode']):
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

    return json.dumps(dict(created_id=shortcode.id))

@minifier.route('/<shortcode>')
def shortcode_route(shortcode):
    """
    Redirect to :shortcode corresponding url after incrementing attribute 'redirect_count'
    and updating attribute 'last_redirect'

    Expect:
        302 if :shortcode found
        404 if :shortcode not found
    """

    shortcode_ = Shortcode.query.filter_by(shortcode=shortcode).first()

    # Raise 404 if shortcode not found
    if not shortcode_:
        abort(HTTPStatus.NOT_FOUND, 'Shortcode not found')

    shortcode_.redirect_count += 1
    shortcode_.last_redirect = datetime.datetime.utcnow()
    db.session.commit()

    return redirect(shortcode_.url)\

@minifier.route('/<shortcode>/stats')
def shortcode_stats_route(shortcode):
    """
    Display attributes for the corresponding :shortcode

    Expect:
        200 if :shortcode found
        404 if :shortcode not found
    """

    shortcode_ = Shortcode.query.filter_by(shortcode=shortcode).first()

    # Raise 404 if shortcode not found
    if not shortcode_:
        abort(HTTPStatus.NOT_FOUND, 'Shortcode not found')

    data = dict(
        created=shortcode_.created.isoformat(timespec='milliseconds') + 'Z',
        lastRedirect=shortcode_.last_redirect.isoformat(timespec='milliseconds') + 'Z' if shortcode_.last_redirect else None,
        redirectCount=shortcode_.redirect_count
    )

    return json.dumps(data)
