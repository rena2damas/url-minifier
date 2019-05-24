from webapp import db
import datetime
import random
import string


class Shortcode(db.Model):
    __tablename__ = 'shortcodes'

    id = db.Column(db.Integer, primary_key=True)
    shortcode = db.Column(db.String(6), nullable=False, unique=True)
    url = db.Column(db.String(2000), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    last_redirect = db.Column(db.DateTime, nullable=True)
    redirect_count = db.Column(db.Integer, nullable=False, default=0)

    # Length for shortcode
    _SHORTCODE_LENGTH = 6

    @classmethod
    def is_valid(cls, code):
        """
        Checks whether :code is valid
        A valid :code has a length of 6 characters and
        contains only alphanumeric characters or underscores
        """
        return len(code) == cls._SHORTCODE_LENGTH and all(c.isalnum() or c == '_' for c in code)

    @classmethod
    def generate_code(cls):
        """
        Generates a new code with 6 characters composed by
        alphanumeric characters or underscores.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits + '_', k=cls._SHORTCODE_LENGTH))
