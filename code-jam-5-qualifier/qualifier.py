import random


def generate_password(
    password_length: int = 8,
    has_symbols: bool = False,
    has_uppercase: bool = False
) -> str:
    """Generates a random password.

    The password will be exactly `password_length` characters.
    If `has_symbols` is True, the password will contain at least one symbol, such as #, !, or @.
    If `has_uppercase` is True, the password will contain at least one upper case letter.
    """

    # Special characters: 32 to 47
    #                     58 to 64
    #                     91 to 96
    #                    123 to 126
    # Digits: 48 to 57
    # Capital : 65 through 90
    # lower case: 97 to 122

    def select_special():
        special_chars = [i for j in (range(32,48), range(58,65), range(91,97), range(123,127)) for i in j]
        #print(str(special_chars))
        #print(str(len(special_chars)))
        random_char = random.randint(0,27)
        #print(str(random_char))
        #print(chr(special_chars[random_char]))
        return chr(special_chars[random_char])

    def select_upper():
        upper_case = chr(random.randint(65,91))
        return upper_case

    def select_any():
        chr(random.randint(32,127))

    def randomize_pos(password_length, has_symbols, has_uppercase):
        return password_length
