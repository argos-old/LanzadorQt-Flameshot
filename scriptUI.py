#!/usr/bin/python3

import os
import subprocess

rutaUi = os.getcwd() + "/lanzadorQt5Flameshot.ui"
rutaOut = os.getcwd() + "/lanzadorQt5FlameshotUI.py"

argui = list()
argui.insert(0, "pyuic5")
argui.insert(1, rutaUi)
argui.append("-o")
argui.append(rutaOut)

proceso = subprocess.run(argui, stdout=subprocess.PIPE)
print(proceso)

