import random, sys


def generate_password(
    password_length: int = 16,
    has_symbols: bool = True,
    has_uppercase: bool = True
) -> str:
    password = randomize_pos(password_length, has_symbols, has_uppercase)
    print(password)
    return password
    
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
    
def sysrnd():
    rnd = random.SystemRandom()
    return rnd

def select_special():
    special_chars = [i for j in (range(32,48), range(58,65), range(91,97), range(123,127)) for i in j]
    random_char = sysrnd().randint(0,27)
    return chr(special_chars[random_char])

def select_upper():
    upper_case = chr(sysrnd().randint(65,91))
    return upper_case

def select_any():
    any_char = chr(sysrnd().randint(32,127))
    return any_char

def rough_generate(length, sym, uppr):
    rough_pass = []

    print("length: " + str(length) + "\n" "Symbol?: " + str(sym) + "\n" "Upper?: " + str(uppr))

    if sym == True and uppr == True:
        length -= 2
    elif sym ==True or uppr == True:
        length -= 1
    else:
        pass

    for i in range(length):
        rough_pass.append(select_any())

    return rough_pass


def randomize_pos(length, sym, uppr):
    password = rough_generate(length, sym, uppr)
    if sym == True:
        sym_index = sysrnd().randint(0,length-1)
        password.insert(sym_index, select_special())
        length += 1
        if uppr == True:
            uppr_index = sysrnd().randint(0,length-1) 
            password.insert(uppr_index, select_upper())
        else:
            pass
    else:
        if uppr == True:
            uppr_index = sysrnd().randint(0,length-1) 
            password.insert(uppr_index, select_upper())
        else:
            pass

    pass_str = ''.join(password)
    return pass_str

generate_password()
