import re


def check_email(email):

    try:
        name, domain = email.split('@') # Will raise ValueError if email consists not of 2 parts
    except ValueError:
        return False

    if not 3 <= len(domain) <= 256:
        return False

    if '.' in domain:
        domain_strings = domain.split('.')
        for string in domain_strings:
            if not re.match('^[a-z0-9_\-]*$', string):
                return False
            if string.endswith('-') or string.startswith('-'):
                return False
    else:
        return False

    if not re.match('^[a-z0-9"\._\-;!,:]*$', name) or len(name) > 128:
        return False

    if '..' in name:
        return False

    if '"' in name:
        name_strings = name.split('"')

        if len(name_strings) % 2 == 0: # Odd number of "
            return False

        for index, string in enumerate(name_strings):
            if index % 2 == 0: # Strings not between "
                if not re.match('^[a-z0-9"\._\-;]*$', string):
                    return False

    return True
