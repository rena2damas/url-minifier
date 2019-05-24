from webapp.models.Shortcode import Shortcode


def test_invalid_code_length():
    """Ensures False when code length is not respected"""

    assert not Shortcode.is_valid('')
    assert not Shortcode.is_valid('ewx12')
    assert not Shortcode.is_valid('ewx1234')

def test_invalid_code_characters():
    """Ensures False when at least one character is invalid"""

    assert not Shortcode.is_valid('ewx12%')
    assert not Shortcode.is_valid('ewx12?')
    assert not Shortcode.is_valid('ewx1?/')

def test_valid_code():
    """Ensures False when at least one character is invalid"""

    assert Shortcode.is_valid('ewx123')
    assert Shortcode.is_valid('ewx12_')
    assert Shortcode.is_valid('123456')
    assert Shortcode.is_valid('ewxewx')
    assert Shortcode.is_valid('______')

def test_generate_code():
    """Ensures a valid code is generated"""

    assert Shortcode.is_valid(Shortcode.generate_code())

