#!/usr/bin/python3
# -*- coding:_UTF-8 -*-

import os
import subprocess
import sys
from configparser import ConfigParser
from PyQt5.QtWidgets import QMessageBox
from lanzadorQt5FlameshotUI import *

# Variables
home = os.getenv("HOME")
rutaArchivoConfig = home + "/.config/LanzadorQt5 Flameshot/Lanzador.cfg"
version = "v.0.1"

if os.path.exists("/usr/local/bin/flameshot"):
    rutaFlameshot = "/usr/local/bin/flameshot"
elif os.path.exists("/usr/bin/flameshot"):
    rutaFlameshot = "/usr/bin/flameshot"

if os.path.exists("/usr/local/share/icons/flameshot.png"):
    rutaIcono = "/usr/local/share/icons/flameshot.png"
elif os.path.exists("/usr/share/icons/flameshot.png"):
    rutaIcono = "/usr/share/icons/flameshot.png"
else:
    rutaIcono = None

# Clases
config = ConfigParser()


class Lanzador(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.ui.lineEditRutaGuardado.setText(home)

        if rutaIcono is not None:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(rutaIcono))
            self.setWindowIcon(icon)

        # Declaración eventos
        self.ui.checkBoxCopiarAlPortapapeles.stateChanged.connect(self.checkbox_copiar_pp_changed)
        self.ui.comboBoxArea.currentIndexChanged.connect(self.combobox_area_click)
        self.ui.spinBoxSegundos.valueChanged.connect(self.spinctrl_segundos_click)
        self.ui.lineEditRutaGuardado.textChanged.connect(self.line_edit_ruta_guardado_click)
        self.ui.toolButtonDirDialog.clicked.connect(self.toolbutton_dir_dialog_click)
        self.ui.pushButtonCaptura.clicked.connect(self.pushbutton_realizar_captura_click)
        self.ui.pushButtonPreferencias.clicked.connect(self.pushbutton_preferencias_click)

        self.set_config()

    def closeEvent(self, a0: QtGui.QCloseEvent):

        try:
            with open(rutaArchivoConfig, "w") as archivoConfig:
                config.write(archivoConfig)

        except Exception as excepcion:
            import sys
            err = ""
            for mj in sys.exc_info():
                err += "! " + str(mj) + "\n"
            self.msg_dlg("Se produjo un error inesperado:", excepcion.args[1], QMessageBox.Ok,
                         QMessageBox.Warning, err)

        finally:
            aplicacion.close()

    def checkbox_copiar_pp_changed(self):

        check = self.ui.checkBoxCopiarAlPortapapeles.isChecked()
        config.set("Configuracion", "copia_clipboard", str(check))

    def combobox_area_click(self):

        indice = self.ui.comboBoxArea.currentIndex()

        self.ui.checkBoxCopiarAlPortapapeles.setEnabled(not indice)
        config.set("Configuracion", "indice_combo", str(indice))

    def spinctrl_segundos_click(self):

        config.set("Configuracion", "retardo", str(self.ui.spinBoxSegundos.value()))

    def line_edit_ruta_guardado_click(self):

        if self.ui.lineEditRutaGuardado.text() == "":
            self.ui.lineEditRutaGuardado.setText(home)

        config.set("Configuracion", "ruta_guardado", self.ui.lineEditRutaGuardado.text())

    def toolbutton_dir_dialog_click(self):

        from PyQt5.QtWidgets import QFileDialog

        dirini = self.ui.lineEditRutaGuardado.text() if os.path.exists(self.ui.lineEditRutaGuardado.text()) else home
        directorio = str(QFileDialog.getExistingDirectory(self, "Seleccione un directorio", dirini))

        self.ui.lineEditRutaGuardado.setText(directorio)
        config.set("Configuracion", "ruta_guardado", directorio)

    def pushbutton_realizar_captura_click(self):

        ok = False

        try:
            if self.check_flameshot() == QMessageBox.No:
                return  # Otras posibilidades: None o QMessagebox.Yes

            import re

            ruta = self.ui.lineEditRutaGuardado.text()

            if not os.path.exists(ruta):
                if bool(re.match(r"(\/[\w^ ]+)+\/?([\w.])+[^.]$", ruta)):
                    os.makedirs(ruta)

                else:
                    self.msg_dlg(ruta, "no es un nombre de directorio válido", QMessageBox.Ok, QMessageBox.Warning)
                    ok = False
                    return

            proceso = subprocess.run(self.set_argumentos(), stdout=subprocess.PIPE)
            salida = proceso.stdout.decode("utf8")

            if salida != "":
                self.msg_dlg("Se produjo un error inesperado al lanzar Flameshot", "", QMessageBox.Ok,
                             QMessageBox.Critical,
                             salida.replace(" See 'flameshot --help'.", ""))
                ok = False

            else:
                ok = True

        except Exception as excepcion:
            import sys

            err = ""
            ok = False

            for mj in sys.exc_info():
                err += "! " + str(mj) + "\n"

            self.msg_dlg("Se produjo un error durante la operación", excepcion.args[1], QMessageBox.Ok,
                         QMessageBox.Warning, err)
        finally:
            if ok:
                self.close()

    @staticmethod
    def pushbutton_preferencias_click():

        subprocess.run([rutaFlameshot, "config"])

    def set_config(self):

        if os.path.exists(rutaArchivoConfig):
            config.read(rutaArchivoConfig)
            self.ui.comboBoxArea.setCurrentIndex(config.getint("Configuracion", "indice_combo"))
            self.ui.spinBoxSegundos.setValue(config.getfloat("Configuracion", "retardo"))
            self.ui.lineEditRutaGuardado.setText(config.get("Configuracion", "ruta_guardado"))
            self.ui.checkBoxCopiarAlPortapapeles.setChecked(config.getboolean("Configuracion", "copia_clipboard"))

        else:
            ruta = rutaArchivoConfig.replace("Lanzador.cfg", "")

            if not os.path.exists(ruta):
                os.makedirs(ruta)

            config.add_section("Configuracion")
            config.set("Configuracion", "indice_combo", "0")
            config.set("Configuracion", "retardo", "0")
            config.set("Configuracion", "ruta_guardado", home)
            config.set("Configuracion", "copia_clipboard", "False")  # Sin implementar (modo full)

            with open(rutaArchivoConfig, "w") as archivoConfig:  # w: sobrescritura: si no existe crea. b: binario
                config.write(archivoConfig)

    def set_argumentos(self):

        argumentos = list()
        argumentos.append(rutaFlameshot)
        argumentos.append("-d")
        argumentos.append(str(int(self.ui.spinBoxSegundos.value() * 1000)))

        if self.ui.lineEditRutaGuardado.text() != "":
            argumentos.append("-p")
            argumentos.append(self.ui.lineEditRutaGuardado.text())

        if self.ui.comboBoxArea.currentIndex():  # Se le toma como bool al tener sólo 2 posibilidades
            argumentos.insert(1, "gui")

        else:
            argumentos.insert(1, "full")

            if self.ui.checkBoxCopiarAlPortapapeles.isChecked():
                argumentos.append("-c")

        return argumentos

    def check_flameshot(self):

        ruta1 = "/usr/local/bin/flameshot"
        ruta2 = "/usr/bin/flameshot"

        if not os.path.exists(ruta1) and not os.path.exists(ruta2):
            return self.msg_dlg("Parece que Flameshot no está instalado.", "¿Desea continuar?",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Question,
                                "Archivo no encontrado en:\n- " + ruta1 + "\n- " + ruta2)

    @staticmethod
    def msg_dlg(txt_cuerpo, txt_adicional="", botones=QMessageBox.Ok, icono=QMessageBox.Information,
                txt_detalles=""):

        msg = QMessageBox()

        msg.setIcon(icono)
        msg.setText(txt_cuerpo)
        msg.setInformativeText(txt_adicional)
        msg.setWindowTitle("Flameshot " + version)
        msg.setStandardButtons(botones)

        if txt_detalles != "":
            msg.setDetailedText(txt_detalles)

        return msg.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    aplicacion = Lanzador()
    aplicacion.show()

    sys.exit(app.exec_())
