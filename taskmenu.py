#! /usr/bin/python3
# -*- coding utf-8 -*-

# @AndreXi (Author)

import os
from subprocess import call
from time import sleep

taskmenu_msg = """--- clock-sync [TASK EDITOR] ---
Puede programar que este script se ejecute automaticamente al iniciar su PC
si esta de acuerdo seleccione CREAR.
Si ha movido la ubicacion de la carpeta clock-sync Elimine y vuelva a Crear la tarea.

Seleccione:
( 1 ) CREAR TAREA
(   )
( 3 ) ELIMINAR TAREA 

( 0 ) SALIR
"""


class TaskEditor():
    """Clase con funciones dedicadas a trabajar con SCHTASKS"""

    def __init__(self, timezone):
        self.taskname = 'clock-sync'
        self.path = os.path.abspath(__file__)
        self.mode = ('/CREATE', '/DELETE', '/CHANGE')
        self.argv = ['SCHTASKS',
                     '/TN',
                     self.taskname]
        self.user_argv = '%s -n' % (timezone)
        self.dirname = os.path.dirname(self.path)
        self.mainpath = os.path.abspath('%s/main.py' % (self.dirname))

    def taskMenu(self):
        """UI de la clase"""
        while True:
            try:
                print('\n' * 5)
                selection = int(input(taskmenu_msg))
                if selection == 0:
                    break
                elif selection == 1:
                    self.makeTask()
                elif selection == 2:
                    # self.editTask()
                    raise ValueError
                elif selection == 3:
                    self.deleteTask()
                else:
                    raise ValueError

            except ValueError:
                print('Seleccion invalida')
                sleep(1)

    def makeTask(self):
        """Prepara los argumentos para crear la tarea"""
        self.argv.insert(1, self.mode[0])   # Modo Crear
        self.xmlEdit(self.path, self.user_argv)
        xmldir = self.xmlFind()             # Guarda la ruta del .xml
        self.argv.append('/XML')            # Agrega los argumentos adicionales
        self.argv.append(xmldir)
        self.do()
        # self.editTask()

    def editTask(self):
        """Edita la ruta y los argumentos de la tarea"""
        self.argv.insert(1, self.mode[2])   # Modo Editar
        # Argumentos para modificar la ruta del main.py
        self.argv.append('/TR')
        add = self.mainpath
        add += ' ' + self.user_argv
        self.argv.append(add)               # Agrega el argumento de /TR
        self.do()

    def deleteTask(self):
        """Elimina la tarea"""
        self.argv.insert(1, self.mode[1])   # Modo Eliminar
        self.do()

    def do(self):
        """Ejecuta el comando con sus argumentos, luego reinicia los argumentos"""
        call(self.argv)
        self.argv_reset()

    def argv_reset(self):
        """Reinicia los argumentos a los iniciales"""
        self.argv = ['SCHTASKS',
                     '/TN',
                     self.taskname]

    def xmlFind(self, todel=0):
        """Busca a clock-sync.xml en el directorio de main.py"""
        xmlpath = os.path.abspath('%s/clock-sync.xml' % (self.dirname))
        if os.path.isfile(xmlpath):
            return xmlpath
        elif todel:
            return None
        else:
            print('No se ha encontrado "clock-sync.xml"\nNo se puede continuar.')
            raise FileNotFoundError

    def xmlEdit(self, path, argv):
        """Modifica el clock-sync.xml"""
        x = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.3" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2019-01-01T01:15:58</Date>
    <Author>AndreXi</Author>
    <Description>Inicia clock-sync para ajustar el reloj, asegurese de estar conectado a internet al momento de ejecutar el script y tener instalado ntplib.</Description>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Enabled>true</Enabled>
    </BootTrigger>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <GroupId>S-1-5-32-544</GroupId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <DisallowStartOnRemoteAppSession>false</DisallowStartOnRemoteAppSession>
    <UseUnifiedSchedulingEngine>false</UseUnifiedSchedulingEngine>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>3</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{}</Command>
      <Arguments>{}</Arguments>
    </Exec>
    <Exec>
      <Command>{}</Command>
      <Arguments>{}</Arguments>
    </Exec>
  </Actions>
</Task>""".format(self.mainpath, self.user_argv,
                  self.mainpath, self.user_argv)

        # Crea y escribe el archivo auxiliar
        with open('clock-sync.xml', 'w') as f:
            f.write(x)

    def xmlDelete(self):
        """Para eliminar el archivo auxiliar 'clock-sync.xml'"""
        if self.xmlFind(todel=1) != None:
            os.remove('clock-sync.xml')
