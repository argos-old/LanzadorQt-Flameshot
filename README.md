# Lanzador-Flameshot
Este script proporciona un diálogo Qt5 en Linux para ejecutar Flameshot. El script permite "recordar" la ruta de guardado y el tiempo de demora

## Importante
Para mí este "proyecto" es un segundo contacto con Python que no pretende ser más que un experimento con este lenguaje y el framework Qt5.

### Requisitos previos:
- Tener instalado Python 3
- Tener instalado el módulo [PyQt5 para Python 3](http://pyqt.sourceforge.net/Docs/PyQt5/installation.html). Un binding de la biblioteca Qt5. Los paquetes están disponibles para varias distribuciones. Por ejemplo, para Ubuntu:
```
sudo apt install python3-pyqt5
```
Opcionalmente se puede descargar e instalar mediante pip3 (válido para cualquier distribución sin precisar permisos root):
```
pip3 install pyqt5
```
- Tener instalado Git (no es necesario si se descargan los scripts de forma manual). Por ejemplo, para Ubuntu:
```
sudo apt install git
```
- [Tener instalado Flameshot](https://github.com/lupoDharkael/flameshot/) (no es imprescindible pero sí recomendable ;)

### Instalación:
```
git clone https://github.com/Arg0s1080/LanzadorQt-Flameshot.git
cd LanzadorQt-Flameshot
python3 instalador.py -v
```
### Desinstalación
```
python3 instalador.py --desinstalar -v
```
### Ayuda
```
python3 instalador.py --help
```
## Errores conocidos:
Como Flameshot lo incluye, se ha incluido la opción de copiar la captura al portapapeles en el modo "pantalla completa", pero, al menos en mi distribución, esta opción no funciona correctamente. 



