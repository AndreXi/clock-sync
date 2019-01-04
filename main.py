#! /usr/bin/python3
# -*- coding utf-8 -*-

# @AndreXi (Author)

""" CLOCK-SYNC
Este programa se encarga de ajustar la hora de un sistema Windows automaticamente
realizado con el objetivo de brindar una solucion rapida a problemas comunes que causan cambios
indeseados en la hora del sistema (Ej: BIOS sin batería, arranque dual).
"""

main_msg = '''Modificar la hora del sistema necesita permisos de Administrador.
Para agilizar puedes pasar como argumento la zona horaria.
Para no entrar en taskmenu use "-n" como argumento
Ej: "main.py -4:00 -n" , "main.py +4:00 -n"'''
print(main_msg)


import os
import sys
import time

import ntplib       # Requiere instalacion

import admin        # Para solicitar privilegios de administrador.
import win32api

from taskmenu import TaskEditor


def main():
    try:
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

        # Ajusta la hora del sistema
        fix_clock(f_time)

        # Sale sin errores.
        return 0

    except ntplib.NTPException:
        print('Ocurrio un error de comunicacion con el servidor\nRevise su conexion a internet, firewalls, etc')
        return 1


def fix_clock(f_time):
    """Aqui se realiza el cambio de hora"""
    win32api.SetSystemTime(f_time[0],   # Año       %Y
                           f_time[1],   # Mes       %m
                           f_time[6],   # dayOfWeek ??
                           f_time[2],   # Dia       %d
                           f_time[3],   # Hora      %H
                           f_time[4],   # Minutos   %M
                           f_time[5],   # Segundos  %S
                           0)           # Milisegundos


def reset_clock():
    """Ajusta el reloj al origen de los tiempos (?)"""
    f_time = time.localtime(0)
    fix_clock(f_time)


def new_TimeZone():
    """Le pide al usuario su zona horaria."""
    print('\n' * 16)
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
            if use_argv:                            # Si el usuario pasa un argumento
                time_zone = sys.argv[1]             # este se usara primero.
            else:
                time_zone = new_TimeZone()          # Pide la la zona horaria
                # La agrega a los argumentos
                sys.argv.append(time_zone)
            # Evita un error por colocar el '+'
            time_zone = time_zone.replace('+', '')
            time_zone = time_zone.rsplit(':')       # Separa horas y minutos
            fix_h = -int(time_zone[0])
            fix_m = -int(time_zone[1])
            return (fix_h, fix_m)                   # Todo esta correcto
        except Exception:
            if use_argv:
                print('ERROR: El argumento no sigue el formato -HH:MM o +HH:MM')
                print('El programa ignorará el argumento')
                use_argv = False                    # Ignorar el argumento erroneo
            else:
                print('ERROR: La información introducida no sigue el formato dado')


if __name__ == '__main__' and os.name == 'nt':
    user_TimeZoneHandler()          # Primero le pide al usuario la zona horaria
    task = TaskEditor(sys.argv[1])  # Y se agrega a los argumentos
    if not admin.isUserAdmin():
        admin.runAsAdmin()          # Se ejecuta en una consola de administrador
        sys.argv.insert(2, '-n')    # Evita que se abra la UI Tareas 2 veces
        admin.runAsAdmin()          # Si, por alguna razon necesito ejecutarlo 2 veces
    else:
        reset_clock()               # Evita errores por reloj muy adelantado
        main()                      # Ajusta el reloj
        if len(sys.argv) > 2:
            if sys.argv[2] == '-n':
                pass
            else:
                print('Para no entrar en taskmenu use "-n" como argumento')
        else:
            task.taskMenu()         # Inicia la UI para tratar la tarea
    task.xmlDelete()                # Elimina el archivo auxiliar
    sys.exit(0)                     # Cierra sin errores
