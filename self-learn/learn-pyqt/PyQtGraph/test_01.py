import pyqtgraph as pg
from PyQt5.QtCore import Qt

# 创建一个PlotWidget
plotWidget = pg.PlotWidget()

# 创建一个曲线
x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 2, 1]
curve = plotWidget.plot(x, y, pen='r', name='sin(x)')

# 添加一个图例对象
legend = plotWidget.addLegend()

# 设置图例对象的位置
legend.setPos(0.9, 0.9)

# 显示PlotWidget
plotWidget.show()
