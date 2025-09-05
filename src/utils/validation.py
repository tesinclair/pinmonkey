from enum import Flag, auto
import re

def inputs_exist(*args):
    for arg in args:
        if type(arg) == int and arg == 0:
            continue
        if not arg:
            raise ValueError(f"Invalid. Input cannot be falsey. Input: \"{arg}\"")

# ==== Password Validation ====

class PasswordValidationFlags(Flag):
    NO_CAPITAL_LETTER = auto()
    NO_NUMBER = auto()
    NO_SPECIAL_CHAR = auto()
    NO_LOWER_CASE = auto()

class PasswordValidationError(ValueError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Invalid Password: {self.message}"



def validate_password(password, flags=None, min_chars=6):
    """
    (src/)utils.validation.validate_password
    
    params:
        password: a string password to validate
        flags: a set of bitwise flags out of PasswordValidationFlags (optional)
        min_chars: an optional change in the minimum number of characters

    returns:
        True: if the password is valid
        raises PasswordValidationError with a clarifying message if the password isn't

    """

    ALLOWED_SPECIAL_CHARS = set("!@#$%^&*()-_+=[]{}|\\:;\"'<>,.?/~`")

    validation_config = {
            "min_chars": min_chars,
            "max_chars": 254,
            "capital_letter": True,
            "special_char": True,
            "number": True,
            "lower_case": True,
    }

    if flags is not None:
        if PasswordValidationFlags.NO_CAPITAL_LETTER in flags:
            validation_config['capital_letter'] = False
        if PasswordValidationFlags.NO_NUMBER in flags:
            validation_config['number'] = False
        if PasswordValidationFlags.NO_SPECIAL_CHAR in flags:
            validation_config['special_char'] = False
        if PasswordValidationFlags.NO_LOWER_CASE in flags:
            validation_config['lower_case'] = False

    # == Validation ==
    if len(password) < validation_config['min_chars']:
        raise PasswordValidationError("Password is too short.")
    if len(password) > validation_config['max_chars']:
        raise PasswordValidationError("Password is too long.")
    if validation_config['capital_letter'] and password.islower():
        raise PasswordValidationError("Password must have a capital letter")
    if validation_config['lower_case'] and password.isupper():
        raise PasswordValidationError("Password must have a lowercase letter")
    if validation_config['number'] and not any(char.isdigit() for char in password):
        raise PasswordValidationError("Password must have a number")
    if validation_config['special_char'] and not any(char in ALLOWED_SPECIAL_CHARS for char in password):
        raise PasswordValidationError("Password must contain a special character")

    return True



        

