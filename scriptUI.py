#!/usr/bin/python3


class CompilaUI:
    def __init__(self, entrada, salida):
        self.entrada = entrada
        self.salida = salida

    def ejecuta(self):
        import subprocess

        argui = list()
        argui.insert(0, "pyuic5")
        argui.insert(1, self.entrada)
        argui.append("-o")
        argui.append(self.salida)

        proceso = subprocess.run(argui, stdout=subprocess.PIPE)

        return proceso




