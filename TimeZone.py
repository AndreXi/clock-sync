#! /usr/bin/python3
# @AndreXi (Author)


def new_TimeZone():
    """Le pide al usuario su zona horaria."""
    instruccions = '''
    A continuación se debe introducir la zona horaria...
    Debe seguir obligatoriamente el siguiente formato:
    -HH:MM                 o                   +HH:MM\n
    '''
    r = input(instruccions)
    with open('timezone.txt', 'w') as f:
        f.write(r)
    return r


def get_TimeZone():
    """
    Lee la zona horaria almacenada en 'timezone.txt'
    """
    try:
        with open('timezone.txt', 'r') as f:
            r = f.read()
        return r
    except Exception:
        return None


if __name__ == '__main__':
    print('Solo se modificará el dato que guarda la zona horaria.')
    new_TimeZone()
