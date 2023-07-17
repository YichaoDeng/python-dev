import pyqtgraph as pg
import numpy as np

# 创建一个PlotWidget
app = pg.mkQApp()
pw = pg.PlotWidget()

# 添加两条曲线
x = np.arange(0, 10, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)
curve1 = pw.plot(x, y1)
curve2 = pw.plot(x, y2)

# 创建十字光标
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine1 = pg.InfiniteLine(angle=0, movable=False)
hLine2 = pg.InfiniteLine(angle=0, movable=False)
pw.addItem(vLine, ignoreBounds=True)
pw.addItem(hLine1, ignoreBounds=True)
pw.addItem(hLine2, ignoreBounds=True)

# 定义鼠标移动事件处理函数
def mouseMoved(evt):
    pos = evt[0]  # 鼠标事件的位置
    if pw.sceneBoundingRect().contains(pos):
        mousePoint = pw.plotItem.vb.mapSceneToView(pos)  # 将鼠标事件的位置转换为视图坐标系中的位置
        x = mousePoint.x()  # 获取x坐标
        y1 = None
        y2 = None
        item1 = None
        item2 = None
        for item in pw.plotItem.listDataItems():  # 遍历所有数据项
            if item.isVisible():
                xData, yData = item.getData()  # 获取数据项的x和y数据
                if xData is not None and yData is not None:
                    index = np.argmin(np.abs(xData - x))  # 找到最接近x坐标的数据点
                    if index < len(yData):
                        if item is curve1:
                            y1 = yData[index]  # 获取对应的y值
                            item1 = item
                        elif item is curve2:
                            y2 = yData[index]  # 获取对应的y值
                            item2 = item
        if y1 is not None:
            vLine.setPos(x)
            hLine1.setPos(y1)
        if y2 is not None:
            vLine.setPos(x)
            hLine2.setPos(y2)

# 将鼠标移动事件处理函数绑定到PlotWidget的鼠标移动事件上
pw.scene().sigMouseMoved.connect(mouseMoved)

# 显示PlotWidget
pw.show()
app.exec_()