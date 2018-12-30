#! /usr/bin/python3
# @AndreXi (Author)

""" CLOCK-SYNC
    Camarero, no le sirva mas a este reloj.
Este programa se encarga de ajustar la hora de un sistema Windows automaticamente
realizado con el objetivo de brindar una solucion rapida a problemas comunes que causan cambios
indeseados en la hora del sistema (Ej: BIOS sin batería, arranque dual).
"""

print('Modificar la hora del sistema necesita permisos de Administrador')
print('Para cambiar la zona horaria ejecute "TimeZone.py"')

import time
import os
import admin    # Para solicitar privilegios de administrador.


err = 'ntplib'  # Para mostrar mensajes de error


def main():
    try:
        import ntplib
        err = 'win32api'
        import win32api

        # Comunicación con NTP.
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')

        # Crea un string con un formato cómodo para configurar la hora.
        f_time = time.strftime('%Y, %m, 0, %d, %H, %M, %S, 0',
                               time.localtime(response.tx_time + zona_horaria()))

        # Separa y organiza todo en una lista.
        f_time = f_time.rsplit(', ')
        for i in range(len(f_time)):
            f_time[i] = int(f_time[i])      # Convierte todo en int.

        # Aqui se realiza el cambio de hora
        win32api.SetSystemTime(f_time[0],   # Año       %Y
                               f_time[1],   # Mes       %m
                               f_time[2],   # dayOfWeek ??
                               f_time[3],   # Dia       %d
                               f_time[4],   # Hora      %H
                               f_time[5],   # Minutos   %M
                               f_time[6],   # Segundos  %S
                               f_time[7])   # Milisegundos

    except ImportError:
        print('Ocurrio un error importando "{}"\nIntente ejecutar "pip3 install {}"'.format(err, err))
    except ntplib.NTPException:
        print('Ocurrio un error de comunicacion con el servidor\nRevise su conexion a internet, firewalls, etc')


def zona_horaria():
    """
    Retorna los segundos que se deben sumar al tiempo NTP obtenido
    """
    from TimeZone import new_TimeZone, get_TimeZone
    while True:
        try:
            time_zone = get_TimeZone()
            time_zone = time_zone.replace('+', '')
            time_zone = time_zone.rsplit(':')
            fix_h = -int(time_zone[0])
            fix_m = -int(time_zone[1])
            fix_s = fix_h * 60 * 60 + fix_m * 60
            return fix_s
        except Exception:
            print('ERROR: La información introducida no sigue el formato dado')
            new_TimeZone()


if __name__ == '__main__':
    if not admin.isUserAdmin() and os.name == 'nt':
        admin.runAsAdmin()
    else:
        main()
