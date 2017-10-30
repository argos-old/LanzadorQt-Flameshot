#!/usr/bin/python
# -*- coding: UTF-8 -*-

##################################################################################
#            Script de instalación lanzador-flameshot.py v 0.2.1                 #
##################################################################################
#                                                                                #
# Ejemplo de utilización 1:                                                      #
#                            Instalar   : python2 instalacion.py                 #
#                            Desinstalar: python2 instalacion.py --desinstalar   #
#                                                                                #
# Ejemplo de utilización 2:               sudo chmod +x instalacion.py           #
#                            Instalar   : ./instalacion.py                       #
#                            Desinstalar: ./python2 instalacion.py --desinstalar #
#                                                                                #
# Se puede mirar, copiar o modificar lo que se desee                             #
#                                                                                #
# Iván Rincón 2017                                                               #
##################################################################################

import os
import shutil
import sys
from configparser import ConfigParser

version = "v.0.2.1"
titulo = "Instalación Lanzador de Flameshot"

print("".ljust(60, "="))
print(titulo + version.rjust(60 - len(titulo) + 1, " "))
print("".ljust(60, "="))


def checkPreguntaSiNo(pregunta):
    rpt = input(pregunta).lower()
    if rpt == "s" or rpt == "si" or rpt == "sí" or rpt == "y" or rpt == "yes":
        return "si"
    elif rpt.lower() == "n" or rpt == "no":
        return "no"
    elif rpt == "":
        return ""
    else:
        print("- Respuesta no válida.")
        return rpt


class Instalacion:
    def __init__(self, desinstalar=False):

        home = os.getenv("HOME")
        rutaScript = home + "/.local/share/lanzador-flameshot/script/"
        rutaLDesktop = home + "/.local/share/applications/lanzador-flameshot.desktop"
        ok = True

        try:
            if not desinstalar:



                if not os.path.exists(rutaScript):
                    os.makedirs(rutaScript)
                if not os.path.exists(rutaScript + "lanzador.py"):
                    shutil.copy(os.getcwd() + "/lanzador-flameshot.py", rutaScript + "lanzador.py")
                    print("- Script copiado")
                else:
                    print("- El script ya existía")

                if not os.path.exists(rutaLDesktop):

                    interprete = input("- ¿Qué intérprete utilizar? [/usr/bin/python] : ")

                    if interprete == "":
                        interprete = "/usr/bin/python"

                    if not os.path.exists(interprete):
                        err = True
                        while err:
                            ine = checkPreguntaSiNo("- " + interprete + " no existe, ¿desea continuar? s / [n] : ")

                            if ine == "no" or ine == "":
                                print("- Operación abortada. Se procede a la desinstalación")
                                Instalacion(True)
                                err = False
                                ok = False
                                exit()

                            if ine == "si":
                                err = False

                    config = ConfigParser()
                    config.optionxform = lambda option: option  # Lee Notas2

                    config.add_section("Desktop Entry")
                    config.set("Desktop Entry", "Encoding", "UTF-8")
                    config.set("Desktop Entry", "Name", "Lanzador Flameshot")
                    config.set("Desktop Entry", "Simple y potente software de captura de pantalla")
                    config.set("Desktop Entry", "Exec", interprete + " " + os.getenv("HOME") +
                               "/.local/share/lanzador-flameshot/script/lanzador.py")
                    config.set("Desktop Entry", "Icon", "/usr/local/share/icons/flameshot.png")
                    config.set("Desktop Entry", "Type", "Application")
                    config.set("Desktop Entry", "Categories", "Graphics;Utility;")

                    with open(rutaLDesktop, "wb") as archivoConfig:
                        config.write(archivoConfig)

                    print("- Lanzador creado")

                else:
                    print("- El lanzador ya existía")

            else:
                trp1 = "- Se eliminó el "
                trp2 = "- No se encontró el "
                rutaConfig = os.getenv("HOME") + "/.config/lanzador-flameshot/Lanzador.cfg"

                if os.path.exists(rutaScript + "lanzador.py"):
                    shutil.rmtree(rutaScript.replace("script/", ""))
                    print(trp1 + "script")
                else:
                    print(trp2 + "script")

                if os.path.exists(rutaLDesktop):
                    os.remove(rutaLDesktop)
                    print(trp1 + "lanzador")
                else:
                    print(trp2 + "lanzador")

                if os.path.exists(rutaConfig):
                    err = True

                    while err:
                        eac = checkPreguntaSiNo("- ¿Eliminar el archivo de configuración? s / [n] : ")

                        if eac == "si":
                            shutil.rmtree(rutaConfig.replace("Lanzador.cfg", ""))
                            print("- Se eliminó el archivo de configuración")
                            err = False
                        elif eac == "no" or eac == "":
                            print("- No se eliminó el archivo de configuración")
                            err = False
                            pass

        except IOError as ex:
            print
            "Error I/O ({0}) : {1}".format(ex.errno, ex.strerror)
            ok &= False

        except Exception:
            print("- Hubo un error inesperado:")
            for mj in sys.exc_info():
                print
                "! " + str(mj)
            ok &= False

        finally:
            if desinstalar:
                cadena = "desinstalación"
            else:
                cadena = "instalación"

            if ok:
                print("- La " + cadena + " se finalizó con éxito")
            else:
                print("- Se produjo un error durante la " + cadena)

            print("".ljust(60, "="))


# Final de clase Instalacion


if __name__ == "__main__":

    d = False

    if len(sys.argv) == 2 and sys.argv[1] == "--desinstalar":
        d = True

    elif len(sys.argv) > 1:
        print("Argumento no válido : " + sys.argv[1] + "\n"
                                                       "Sintaxis ...........: instalacion.py [--desinstalar]")
        exit()

    else:

        if not os.path.exists("/usr/local/bin/flameshot") and not os.path.exists("/usr/bin/flameshot"):
            err = True
            while err:
                res = checkPreguntaSiNo("- Parece que Flameshot no está instalado.\n¿Desea continuar? [s] / n :")
                if res == "si" or res == "":
                    Instalacion()
                elif res == "no":
                    print("- Instalación abortada")
                    print("".ljust(60, "="))
                    exit()

    Instalacion(d)