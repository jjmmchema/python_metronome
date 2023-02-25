import sys
import threading
import time

from PyQt6.QtSvg import QSvgRenderer
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget

from metronome import Metronome


class Window(QtWidgets.QMainWindow):

    rotationSignal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setGeometry(60, 60, 1200, 600)

        self.layout = QtWidgets.QVBoxLayout()    

        self.rotationSignal.connect(self.rotateMetronome)

        self.metronome = Metronome()

        self.slider = QtWidgets.QSlider(minimum=-90, maximum=90, orientation=Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.metronome.pendulumProxy.setRotation)

        self.resetBtn = QtWidgets.QPushButton("Reset")
        self.resetBtn.setFixedWidth(100)
        self.resetBtn.clicked.connect(self.resetMetronome)

        self.layout.addWidget(self.resetBtn, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.metronome, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.slider)

        w = QtWidgets.QWidget()
        w.setLayout(self.layout)
        self.setCentralWidget(w)
        self.show()

    @QtCore.pyqtSlot(bool)
    def rotateMetronome(self, status):

        if self.metronome.getRotation() in [-90, 90]:
            self.metronome.direction *= -1

        self.metronome.addToRotation(1)
        self.slider.setValue(int(self.metronome.getRotation()))

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_R:
            self.resetMetronome()
        elif event.key() == Qt.Key.Key_Space:
            if self.metronome.isRunning == False:
                threading.Thread(target=self.startMetronome).start()
        elif event.key() == Qt.Key.Key_Escape:
            self.resetMetronome()

    def startMetronome(self):
        self.metronome.start()

        while self.metronome.isRunning:
            self.rotationSignal.emit(True)
            time.sleep(1)    

    def resetMetronome(self):
        self.metronome.stop()
        self.slider.setValue(0)

def loadStyleSheet(app: QtWidgets.QApplication, path: str="src/styles.qss") -> None:
    with open(path, "r") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    
    loadStyleSheet(App)

    Window = Window()
    sys.exit(App.exec())
