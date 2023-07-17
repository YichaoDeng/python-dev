from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QTransform
from PyQt5.QtGui import QBrush, QColor
import sys
from PyQt5.QtWidgets import QApplication

# 创建一个场景和视图
app = QApplication(sys.argv)
scene = QGraphicsScene()
view = QGraphicsView(scene)
# 创建矩形图形项
rect = QGraphicsRectItem(QRectF(50, 50, 100, 100))

# 设置矩形的颜色和填充
brush = QBrush(Qt.red)
rect.setBrush(brush)

# 将矩形添加到场景中
scene.addItem(rect)

# 第一次旋转
center1 = rect.mapToScene(rect.boundingRect().center())
transform1 = QTransform().translate(center1.x(), center1.y()).rotate(
    45).translate(-center1.x(), -center1.y())
rect.setTransform(transform1)

# 第二次旋转
center2 = rect.mapToScene(rect.boundingRect().center())
transform2 = QTransform().translate(center2.x() + 100, center2.y()).rotate(30).translate(-center2.x(), -center2.y())
rect.setTransform(transform2, True)

# 显示视图
view.show()
sys.exit(app.exec_())
