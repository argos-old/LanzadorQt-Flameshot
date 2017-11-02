#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#############################################################
#   Script de instalación Lanzador Qt5 Flameshot.py v 0.1   #
#############################################################
#                                                           #
# Uso 1:             python3 instalacion.py --help          #
#                                                           #
# Uso 2:             sudo chmod +x instalacion.py           #
#                    ./instalacion.py --help                #
#                                                           #
# Se puede mirar, copiar o modificar lo que se desee        #
#                                                           #
# Iván Rincón 2017                                          #
#############################################################

import argparse
import os
import shutil
from configparser import ConfigParser

import scriptUI

version = "v.0.1"
titulo = "Instalación Lanzador Qt5 de Flameshot"

print("".ljust(60, "="))
print(titulo + version.rjust(60 - len(titulo), " "))
print("".ljust(60, "="))


def check_pregunta_si_no(pregunta):

    rpt = input(pregunta).lower()

    if rpt in ("s", "si", "sí", "y", "yes"):
        return "si"
    elif rpt in ("n", "no"):
        return "no"
    elif rpt == "":
        return rpt
    else:
        print("-", "Respuesta no válida.")
        return None


class Instalacion:
    def __init__(self):

        home = os.getenv("HOME")
        ruta_script = home + "/.local/share/LanzadorQt5Flameshot/script/"
        ruta_l_desktop = home + "/.local/share/applications/lanzador-flameshot.desktop"
        ok = True

        try:
            if args.devmode:
                print("-", args)
                if args.desinstalar:
                    print("-", "Devmode sólo está disponible durante la instalación")
                    exit()

                entrada = os.getcwd() + "/lanzadorQt5Flameshot.ui"
                salida = os.getcwd() + "/lanzadorQt5FlameshotUI.py"

                compilaui = scriptUI.CompilaUI(entrada, salida)
                proceso_finalizado = compilaui.ejecuta()
                print("-", "args ......:", proceso_finalizado.args)
                print("-", "stdout ....:", proceso_finalizado.stdout.decode("utf8"))
                print("-", "returncode :", proceso_finalizado.returncode)

            if not args.desinstalar:
                if not os.path.exists(ruta_script):
                    os.makedirs(ruta_script)
                if not os.path.exists(ruta_script + "lanzadorQt5.py"):
                    shutil.copy(os.getcwd() + "/lanzadorQt5Flameshot.py", ruta_script + "lanzadorQt5.py")
                    if args.verbose:
                        print("-", "Script copiado")

                else:
                    if args.verbose:
                        print("-", "El script ya existía")

                if not os.path.exists(ruta_script + "lanzadorQt5FlameshotUI.py"):
                    shutil.copy(os.getcwd() + "/lanzadorQt5FlameshotUI.py", ruta_script + "lanzadorQt5FlameshotUI.py")
                    if args.verbose:
                        print("-", "Interface de usuario Qt5 copiada")

                else:
                    if args.verbose:
                        print("-", "La interfaz Qt5 ya existía")

                if not os.path.exists(ruta_l_desktop):

                    interprete = input("- ¿Qué intérprete utilizar? [/usr/bin/python3] : ")

                    if interprete == "":
                        interprete = "/usr/bin/python3"

                    if not os.path.exists(interprete):
                        err = True
                        while err:
                            ine = check_pregunta_si_no("- " + interprete + " no existe, ¿desea continuar? s / [n] : ")

                            if ine == "no" or ine == "":
                                print("-", "Operación abortada. Se procede a la desinstalación")
                                args.desinstalar = True
                                Instalacion()
                                err = None
                                ok = False
                                exit()

                            if ine == "si":
                                err = None

                    config = ConfigParser()
                    config.optionxform = lambda option: option  # Lee Notas2

                    config.add_section("Desktop Entry")
                    config.set("Desktop Entry", "Encoding", "UTF-8")
                    config.set("Desktop Entry", "Name", "Lanzador Qt5 Flameshot")
                    config.set("Desktop Entry", "Comment", "Simple y potente software de captura de pantalla")
                    config.set("Desktop Entry", "Exec", interprete + " " + ruta_script + "lanzadorQt5.py")
                    config.set("Desktop Entry", "Icon", "/usr/local/share/icons/flameshot.png")
                    config.set("Desktop Entry", "Type", "Application")
                    config.set("Desktop Entry", "Categories", "Graphics;Utility;")

                    with open(ruta_l_desktop, "w") as archivoConfig:
                        config.write(archivoConfig)
                    if args.verbose:
                        print("-", "Lanzador creado")

                else:
                    if args.verbose:
                        print("-", "El lanzador ya existía")

            elif args.desinstalar:
                if args.verbose:
                    trp1 = "- Se eliminó "
                    trp2 = "- No se encontró "

                ruta_config = os.getenv("HOME") + "/.config/LanzadorQt5 Flameshot/Lanzador.cfg"

                if os.path.exists(ruta_script + "lanzadorQt5.py") or os.path.exists(ruta_script + "lanzadorQT5UI.py"):
                    shutil.rmtree(ruta_script.replace("script/", ""))
                    if args.verbose:
                        print(trp1 + "el script")
                        print(trp1 + "la interface Qt5")

                else:
                    if args.verbose:
                        print(trp2 + "el script")
                        print(trp2 + "la interface Qt5")

                if os.path.exists(ruta_l_desktop):
                    os.remove(ruta_l_desktop)
                    if args.verbose:
                        print(trp1 + "el lanzador")

                else:
                    if args.verbose:
                        print(trp2 + "el lanzador")

                if os.path.exists(ruta_config):
                    err = True
                    while err:
                        eac = check_pregunta_si_no("- ¿Eliminar el archivo de configuración? s / [n] : ")

                        if eac == "si":
                            shutil.rmtree(ruta_config.replace("Lanzador.cfg", ""))
                            if args.verbose:
                                print("-", "Se eliminó el archivo de configuración")
                            err = None
                        elif eac == "no" or eac == "":
                            if args.verbose:
                                print("-", "No se eliminó el archivo de configuración")
                            err = None

        except IOError as ex:
            print("!", "Error I/O ({0}) : {1}".format(ex.errno, ex.strerror))
            ok &= False

        except Exception:
            import sys
            print("-", "Hubo un error inesperado:")
            for mj in sys.exc_info():
                print("!", str(mj))
            ok &= False

        finally:
            if args.desinstalar:
                cadena = "desinstalación"

            else:
                cadena = "instalación"

            if ok:
                print("-", "La " + cadena + " se finalizó con éxito")

            else:
                print("-", "Se produjo un error durante la " + cadena)

            print("".ljust(60, "="))

            exit()

# Final de clase Instalacion


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Instalador del Lanzador Qt5 para Flameshot')
    parser.add_argument("-d", "--desinstalar", action="store_true",
                        help="Desinstala por completo el lanzador y los archivos de configuración")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Detalla el proceso en la línea de comandos")
    parser.add_argument("--devmode", action="store_true",
                        help="Realiza la instalación utilizando las librerías de desarrollo de PyQt. Esta "
                             "opción no es necesaria en absoluto")
    args = parser.parse_args()

    if not args.desinstalar:
        if not os.path.exists("/usr/local/bin/flameshot") and not os.path.exists("/usr/bin/flameshot"):
            err = True
            while err:
                res = check_pregunta_si_no("- Parece que Flameshot no está instalado.\n¿Desea continuar? [s] / n :")
                if res == "si" or res == "":
                    err = None
                    Instalacion()
                elif res == "no":
                    print("-", "Instalación abortada")
                    print("".ljust(60, "="))
                    exit()

    Instalacion()
