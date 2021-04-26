from PyQt5 import QtGui, QtWidgets


class Line(QtWidgets.QGraphicsLineItem):
    """Линия."""

    def __init__(self, startPos: tuple, endPos: tuple):
        super().__init__(*startPos, *endPos)
        self.startPos = startPos
        self.endPos = endPos
        self.setPen(QtGui.QColor(0, 0, 0))

    def updatePos(self, startPos=None, endPos=None):
        """Обновить позицию линии."""
        self.startPos = startPos or self.startPos
        self.endPos = endPos or self.endPos
        self.setLine(*self.startPos, *self.endPos)


class Edge(Line):
    """Ребро, соединяющее два блока."""

    def __init__(self, start, end):
        super().__init__(start.centerPos(), end.centerPos())
        self.start = start
        self.end = end

    def startBlock(self):
        """Возвращает начальный блок ребра."""
        return self.start.parentItem()

    def endBlock(self):
        """Возвращает конечный блок ребра."""
        return self.end.parentItem()

    def updatePos(self):
        """Обновить позицию ребра."""
        super().updatePos(self.start.centerPos(), self.end.centerPos())

    def remove(self):
        """Удалить ребро."""
        self.start.edge = None
        self.start.widget.setChecked(False)
        self.end.edge = None
        self.end.widget.setChecked(False)
        self.scene().removeItem(self)
