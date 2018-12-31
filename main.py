#! /usr/bin/python3
# @AndreXi (Author)

""" CLOCK-SYNC
    Camarero, no le sirva mas a este reloj.
Este programa se encarga de ajustar la hora de un sistema Windows automaticamente
realizado con el objetivo de brindar una solucion rapida a problemas comunes que causan cambios
indeseados en la hora del sistema (Ej: BIOS sin batería, arranque dual).
"""

print('Modificar la hora del sistema necesita permisos de Administrador')
print('Para agilizar puedes pasar como argumento la zona horaria')

import time
import os
import admin    # Para solicitar privilegios de administrador.
import sys


err = 'ntplib'  # Para mostrar mensajes de error.


def main():
    try:
        import ntplib
        err = 'win32api'
        import win32api

        # Comunicación con NTP.
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')

        # Variables
        user_tz = user_TimeZoneHandler()
        user_timezone = user_tz[0] * 60 * 60 + user_tz[1] * 60
        local_timezone = time.timezone
        offset = local_timezone * 2 - user_timezone

        # Genera la tupla con la hora actualizada
        f_time = time.localtime(response.tx_time + offset)

        # Aqui se realiza el cambio de hora
        win32api.SetSystemTime(f_time[0],   # Año       %Y
                               f_time[1],   # Mes       %m
                               f_time[6],   # dayOfWeek ??
                               f_time[2],   # Dia       %d
                               f_time[3],   # Hora      %H
                               f_time[4],   # Minutos   %M
                               f_time[5],   # Segundos  %S
                               0)           # Milisegundos

    except ImportError:
        print('Ocurrio un error importando "{}"\nIntente ejecutar "pip3 install {}"'.format(err, err))
    except ntplib.NTPException:
        print('Ocurrio un error de comunicacion con el servidor\nRevise su conexion a internet, firewalls, etc')


def new_TimeZone():
    """Le pide al usuario su zona horaria."""
    instruccions = '''
    A continuación se debe introducir la zona horaria...
    Debe seguir obligatoriamente el siguiente formato:
    -HH:MM                 o                   +HH:MM\n
    '''
    r = input(instruccions)
    return r


def user_TimeZoneHandler():
    """
    Retorna una tupla con la zona horaria guardados como enteros
    """
    # Si se pasa la zona horaria como argumento se usará primero.
    if len(sys.argv) > 1:
        use_argv = True
    else:
        use_argv = False

    while True:
        try:
            if use_argv:
                time_zone = sys.argv[1]
            else:
                time_zone = new_TimeZone()
            time_zone = time_zone.replace('+', '')
            time_zone = time_zone.rsplit(':')
            fix_h = -int(time_zone[0])
            fix_m = -int(time_zone[1])
            return (fix_h, fix_m)
        except Exception:
            if use_argv:
                print('ERROR: El argumento no sigue el formato -HH:MM o +HH:MM')
                print('El programa ignorará el argumento')
                use_argv = False
            else:
                print('ERROR: La información introducida no sigue el formato dado')
                new_TimeZone()


if __name__ == '__main__':
    if not admin.isUserAdmin() and os.name == 'nt':
        admin.runAsAdmin()
    else:
        main()
