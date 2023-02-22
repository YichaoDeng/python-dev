import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QGraphicsScene, QGraphicsView, QVBoxLayout, \
    QGraphicsEllipseItem


class Window(QMainWindow):
    view: QGraphicsView
    view_2: QGraphicsView
    scene: QGraphicsScene
    v_layout: QVBoxLayout
    central_widget: QWidget
    e_item: QGraphicsEllipseItem

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setup_ui()
        self.setup_scene()

    def setup_ui(self):
        self.resize(600, 600)
        self.setWindowTitle('Custom Graphics View')
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.v_layout = QVBoxLayout(self.central_widget)

    def setup_scene(self):
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.view.setSceneRect(-300, -300, 900, 900)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scene.setBackgroundBrush(Qt.lightGray)
        self.scene.setSceneRect(-300, -300, 900, 900)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.v_layout.addWidget(self.view)  # noqa
        self.e_item = QtWidgets.QGraphicsEllipseItem(0, 0, 300, 300)
        self.scene.addItem(self.e_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
