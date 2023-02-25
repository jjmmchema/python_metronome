from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget


class Metronome(QtWidgets.QGraphicsView):

    def __init__(self) -> None:
        super().__init__()

        self.isRunning = False
        self.direction = -1

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )

        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.border = QSvgWidget("src/metronome_border.svg")
        self.pendulum = QSvgWidget("src/line.svg")

        self.scene = QtWidgets.QGraphicsScene()

        self.setSceneRect(QtCore.QRectF(self.rect()))
        self.setScene(self.scene)

        self.borderProxy = self.scene.addWidget(self.border)
        self.borderProxy.moveBy(1.5, 0)
        # self.borderProxy.setTransformOriginPoint(self.proxy.boundingRect().center())

        self.pendulumProxy = self.scene.addWidget(self.pendulum)
        self.pendulumProxy.moveBy(199, 0)
        xpos, ypos = self.pendulumProxy.boundingRect().width()/2, self.pendulumProxy.boundingRect().bottom()
        self.pendulumProxy.setTransformOriginPoint(QtCore.QPointF(xpos, ypos))

    
    def start(self) -> None:
        self.isRunning = True

    def stop(self) -> None:
        self.isRunning = False
        self.reset()

    def getRotation(self) -> float:
        return self.pendulumProxy.rotation()
    
    def setRotation(self, angle: float) -> None:
        self.pendulumProxy.setRotation(angle)

    def addToRotation(self, amount: float) -> None:
        self.setRotation(self.getRotation() + amount * self.direction)

    def reset(self) -> None:
        self.setRotation(0)
        self.direction = -1

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(600, 310)

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        bounds = self.scene.itemsBoundingRect()
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
