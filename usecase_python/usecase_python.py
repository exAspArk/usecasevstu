#!/usr/bin/env python
# coding: windows-1251
# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QString', 2)


import math

from PySide import QtCore, QtGui

import diagramscene_rc

# базовый класс для линии
class TotalLineDiagram(QtGui.QGraphicsLineItem):
     def __init__(self, startItem, endItem, parent=None, scene=None):
         super(TotalLineDiagram, self).__init__(parent, scene)
         self.myStartItem = startItem
         self.myEndItem = endItem

         self.arrowHead = QtGui.QPolygonF()

         self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
         self.myColor = QtCore.Qt.black
         self.setPen(QtGui.QPen(self.myColor, 2, QtCore.Qt.SolidLine,
                QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
         self.arrowsComment = []

     def boundingRect(self):
        extra = (self.pen().width() + 20) / 2.0
        p1 = self.line().p1()
        p2 = self.line().p2()
        return QtCore.QRectF(p1, QtCore.QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized().adjusted(-extra, -extra, extra, extra)
     
     def setColor(self, color):
        self.myColor = color

     def startItem(self):
        return self.myStartItem

     def endItem(self):
        return self.myEndItem

     def shape(self):
        path = super(TotalLineDiagram, self).shape()
        path.addPolygon(self.arrowHead)
        return path

     def updatePosition(self):
        line = QtCore.QLineF(self.mapFromItem(self.myStartItem, 0, 0), self.mapFromItem(self.myEndItem, 0, 0))
        self.setLine(line)
     # функция которую надо описать для дочеррних классов
     # определяет для начала и конца стрелки нужно ли её рисовать
     # return true - если нужно, false - если не нужно отрисовывать
     def isValid(self):
         pass
     def polygon(self):
         return QtGui.QPolygonF(self.boundingRect())
     def addArrow(self,item):
         self.arrowsComment.append(item)
         
# клас для отрисовки линии комментария
class CommentLine(TotalLineDiagram):
    def __init__(self, startItem, endItem, parent=None, scene=None):
        super(CommentLine,self).__init__(startItem,endItem,parent,scene)

    def isValid(self):
        if((isinstance(self.startItem(),Comment) and \
            isinstance(self.endItem(), TotalLineDiagram)) or \
            (isinstance(self.startItem(), TotalLineDiagram) and \
            isinstance(self.endItem(), Comment))):
            return True
        else: return False

    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return
        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        # отрисовка пунктиром
        myPen.setStyle(QtCore.Qt.DotLine)
        myPen.setColor(self.myColor)
        arrowSize = 20.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        centerLine = QtCore.QLineF(myStartItem.pos(), myEndItem.pos())
        endPolygon = myEndItem.polygon()
        p1 = endPolygon.at(0) + myEndItem.pos()

        intersectPoint = QtCore.QPointF()
        for i in endPolygon:
            p2 = i + myEndItem.pos()
            polyLine = QtCore.QLineF(p1, p2)
            intersectType, intersectPoint = polyLine.intersect(centerLine)
            if intersectType == QtCore.QLineF.BoundedIntersection:
                break
            p1 = p2

        self.setLine(QtCore.QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrowP1 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)

        self.arrowHead.clear()
        for point in [line.p1(), arrowP1, arrowP2]:
            self.arrowHead.append(point)

        painter.drawLine(line)
        # убрали отрисовку бошки у стрелки
        # painter.drawPolygon(self.arrowHead)
        if self.isSelected():
            painter.setPen(QtGui.QPen(myColor, 1, QtCore.Qt.DashLine))
            myLine = QtCore.QLineF(line)
            myLine.translate(0, 4.0)
            painter.drawLine(myLine)
            myLine.translate(0,-8.0)
            painter.drawLine(myLine)
    def polygon(self):
         return QtGui.QPolygonF(self.boundingRect())

# класс для отрисовки стрелки ассоциации
class ArrowAssociation(TotalLineDiagram):
    def __init__(self, startItem, endItem, parent=None, scene=None):
        super(ArrowAssociation,self).__init__(startItem,endItem,parent,scene)

    def isValid(self):
        if((isinstance(self.startItem(),Actor) and \
            isinstance(self.endItem(), UseCase)) or \
            (isinstance(self.startItem(), UseCase) and \
            isinstance(self.endItem(), Actor))):
            return True
        elif ((isinstance(self.startItem(),Actor) and \
            isinstance(self.endItem(), Actor))):
            return True
        elif ((isinstance(self.startItem(),UseCase) and \
            isinstance(self.endItem(), UseCase))):
            return True
        else: return False

    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return

        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        myPen.setColor(self.myColor)
        arrowSize = 20.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        centerLine = QtCore.QLineF(myStartItem.pos(), myEndItem.pos())
        endPolygon = myEndItem.polygon()
        p1 = endPolygon.at(180) + myEndItem.pos()

        intersectPoint = QtCore.QPointF()
        for i in endPolygon:
            p2 = i + myEndItem.pos()
            polyLine = QtCore.QLineF(p1, p2)
            intersectType, intersectPoint = polyLine.intersect(centerLine)
            if intersectType == QtCore.QLineF.BoundedIntersection:
                break
            p1 = p2

        self.setLine(QtCore.QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrowP1 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)

        self.arrowHead.clear()
        for point in [line.p1(), arrowP1, arrowP2]:
            self.arrowHead.append(point)

        painter.drawLine(line)
        painter.drawPolygon(self.arrowHead)
        if self.isSelected():
            painter.setPen(QtGui.QPen(myColor, 1, QtCore.Qt.DashLine))
            myLine = QtCore.QLineF(line)
            myLine.translate(0, 4.0)
            painter.drawLine(myLine)
            myLine.translate(0,-8.0)
            painter.drawLine(myLine)
    def polygon(self):
         return QtGui.QPolygonF(self.boundingRect())


# класс для отрисовки стрелки обобщения
class ArrowGeneralization(TotalLineDiagram):
    def __init__(self, startItem, endItem, parent=None, scene=None):
        super(ArrowGeneralization,self).__init__(startItem,endItem,parent,scene)

    def isValid(self):
        if ((isinstance(self.startItem(),Actor) and \
            isinstance(self.endItem(), Actor)) or \
            (isinstance(self.startItem(), UseCase) and \
            isinstance(self.endItem(), UseCase))):
            return True
        else: return False
    
    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return

        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        myPen.setColor(self.myColor)
        arrowSize = 20.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        centerLine = QtCore.QLineF(myStartItem.pos(), myEndItem.pos())
        endPolygon = myEndItem.polygon()
        p1 = endPolygon.at(180) + myEndItem.pos()

        intersectPoint = QtCore.QPointF()
        for i in endPolygon:
            p2 = i + myEndItem.pos()
            polyLine = QtCore.QLineF(p1, p2)
            intersectType, intersectPoint = polyLine.intersect(centerLine)
            if intersectType == QtCore.QLineF.BoundedIntersection:
                break
            p1 = p2

        self.setLine(QtCore.QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrowP1 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)

        self.arrowHead.clear()
        for point in [line.p1(),arrowP1,arrowP2]:
             self.arrowHead.append(point)

        painter.drawLine(line)
        painter.drawPolygon(self.arrowHead)
        if self.isSelected():
            painter.setPen(QtGui.QPen(myColor, 1, QtCore.Qt.DashLine))
            myLine = QtCore.QLineF(line)
            myLine.translate(0, 4.0)
            painter.drawLine(myLine)
            myLine.translate(0,-8.0)
            painter.drawLine(myLine)
    def polygon(self):
         return QtGui.QPolygonF(self.boundingRect())
            
class ElementDiagramm(QtGui.QGraphicsTextItem):
    CommentType,UseCaseType,ActorType,NoneType = range(4)
    
    lostFocus = QtCore.Signal(QtGui.QGraphicsTextItem)

    selectedChange = QtCore.Signal(QtGui.QGraphicsItem)

    def __init__(self, parent=None, scene=None):
        super(ElementDiagramm, self).__init__(parent, scene)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.myTypeElement = ElementDiagramm.NoneType

        self.arrows = []

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            self.selectedChange.emit(self)
        return value

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.lostFocus.emit(self)
        super(ElementDiagramm, self).focusOutEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == QtCore.Qt.NoTextInteraction:
            self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        super(ElementDiagramm, self).mouseDoubleClickEvent(event)
        
    def typeElement(self):
        return self.myTypeElement

    def polygon(self):
        return QtGui.QPolygonF(self.boundingRect())

    def addArrow(self,item):
        self.arrows.append(item)

class Comment(ElementDiagramm):
    def __init__(self, parent=None, scene=None):
        super(Comment, self).__init__(parent, scene)
        self.myTypeElement = ElementDiagramm.CommentType

    def paint(self, painter, option, widget=None):
        bodyRect = self.boundingRect()
        pointStart =  QtCore.QPointF((bodyRect.topRight().x()- bodyRect.topLeft().x())*9.0/10.0,
			bodyRect.topLeft().y());
        pointEnd = QtCore.QPointF(bodyRect.topRight().x(),
			(bodyRect.bottomRight().y() - bodyRect.topRight().y())*1.0/10.0)

        linearGrad = QtGui.QLinearGradient(pointEnd, bodyRect.bottomLeft())

        linearGrad.setColorAt(0, QtCore.Qt.white)
        linearGrad.setColorAt(1, QtGui.QColor(255,130,80))
        painter.fillRect(bodyRect,QtGui.QBrush(linearGrad))

        painter.drawLine(bodyRect.topLeft(),pointStart)
        painter.drawLine(bodyRect.topLeft(),bodyRect.bottomLeft())
        painter.drawLine(bodyRect.bottomLeft(),bodyRect.bottomRight())
        painter.drawLine(bodyRect.bottomRight(),pointEnd)
        painter.drawLine(pointStart,pointEnd)
        painter.drawLine(pointStart,QtCore.QPointF(pointStart.x(),pointEnd.y()))
        painter.drawLine(QtCore.QPointF(pointStart.x(),pointEnd.y()),pointEnd)
        super(Comment, self).paint(painter, option, widget)
    def polygon(self):
        return QtGui.QPolygonF(self.boundingRect())

class UseCase(ElementDiagramm):
    def __init__(self, parent=None, scene=None):
        super(UseCase, self).__init__(parent, scene)
        self.myTypeElement = ElementDiagramm.UseCaseType

    def paint(self, painter, option, widget=None):
        bodyRect = self.boundingRect()
        #painter.drawEllipse(bodyRect)
        listCoord = bodyRect.getCoords()
        x1 = listCoord[0]
        y1 = listCoord[1]
        x2 = listCoord[2]
        y2 = listCoord[3]
        grad = QtGui.QRadialGradient(QtCore.QPointF(x1,y1),bodyRect.width())
        grad.setColorAt(1,QtGui.QColor(255,160,25))
        grad.setColorAt(0.5,QtCore.Qt.yellow)
        grad.setColorAt(0,QtCore.Qt.white)
        _path = QtGui.QPainterPath()
        _path.addEllipse(bodyRect)
        painter.fillPath(_path,QtGui.QBrush(grad))
        super(UseCase, self).paint(painter, option, widget)
    def polygon(self):
        return QtGui.QPolygonF(self.boundingRect())

class Actor(ElementDiagramm):
    def __init__(self, parent=None, scene=None):
        super(Actor, self).__init__(parent, scene)
        self.myTypeElement = ElementDiagramm.ActorType
        self.setTextWidth(50);
        self.setHtml("<img src=\":/images/actor.png\" /><p>Actor</p>");

    def paint(self, painter, option, widget=None):
        super(Actor, self).paint(painter, option, widget)
    def polygon(self):
        return QtGui.QPolygonF(self.boundingRect())

class DiagramScene(QtGui.QGraphicsScene):
    InsertItem, InsertLine, InsertText, MoveItem,InsertCommentLine,InsertUseCase,InsertArrowAssociation,InsertArrowGeneralization,InsertActor  = range(9)

    itemInserted = QtCore.Signal(ElementDiagramm)

    textInserted = QtCore.Signal(QtGui.QGraphicsTextItem)

    itemSelected = QtCore.Signal(QtGui.QGraphicsItem)

    def __init__(self, itemMenu, parent=None):
        super(DiagramScene, self).__init__(parent)

        self.myItemMenu = itemMenu
        self.myMode = self.MoveItem
        #self.myItemType = DiagramItem.Step
        self.line = None
        self.textItem = None
        self.myItemColor = QtCore.Qt.white
        self.myTextColor = QtCore.Qt.black
        self.myLineColor = QtCore.Qt.black
        self.myFont = QtGui.QFont()

    def setLineColor(self, color):
        self.myLineColor = color
        if self.isItemChange(Arrow):
            item = self.selectedItems()[0]
            item.setColor(self.myLineColor)
            self.update()

    def setTextColor(self, color):
        self.myTextColor = color
        if self.isItemChange(Comment):
            item = self.selectedItems()[0]
            item.setDefaultTextColor(self.myTextColor)

    def setItemColor(self, color):
        self.myItemColor = color
        if self.isItemChange(ElementDiagram):
            item = self.selectedItems()[0]
            item.setBrush(self.myItemColor)

    def setFont(self, font):
        self.myFont = font
        if self.isItemChange(Comment):
            item = self.selectedItems()[0]
            item.setFont(self.myFont)

    def setMode(self, mode):
        self.myMode = mode

    def setItemType(self, type):
        self.myItemType = type

    def editorLostFocus(self, item):
        cursor = item.textCursor()
        cursor.clearSelection()
        item.setTextCursor(cursor)

        if not item.toPlainText():
            self.removeItem(item)
            item.deleteLater()

    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != QtCore.Qt.LeftButton):
            return
        if self.myMode == self.InsertArrowAssociation or self.myMode == self.InsertArrowGeneralization or self.myMode == self.InsertCommentLine:
            self.line = QtGui.QGraphicsLineItem(QtCore.QLineF(mouseEvent.scenePos(),
                                        mouseEvent.scenePos()))
            self.line.setPen(QtGui.QPen(self.myLineColor, 2))
            self.addItem(self.line)
        elif self.myMode == self.InsertText:
            textItem = Comment()
        elif self.myMode == self.InsertUseCase:
            textItem = UseCase()
        elif self.myMode == self.InsertActor:
            textItem = Actor()
        if self.myMode == self.InsertText or self.myMode == self.InsertUseCase or \
           self.myMode == self.InsertActor:
            textItem.setFont(self.myFont)
            textItem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            textItem.setZValue(1000.0)
            textItem.lostFocus.connect(self.editorLostFocus)
            textItem.selectedChange.connect(self.itemSelected)
            self.addItem(textItem)
            textItem.setDefaultTextColor(self.myTextColor)
            textItem.setPos(mouseEvent.scenePos())
            self.textInserted.emit(textItem)
        super(DiagramScene, self).mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if (self.myMode == self.InsertArrowAssociation or self.myMode == self.InsertArrowGeneralization or self.myMode == self.InsertCommentLine)  and self.line :
            newLine = QtCore.QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)
        elif self.myMode == self.MoveItem:
            super(DiagramScene, self).mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        if self.line and (self.myMode == self.InsertArrowAssociation or self.myMode == self.InsertArrowGeneralization or self.myMode == self.InsertCommentLine):
            startItems = self.items(self.line.line().p1())
            if len(startItems) and startItems[0] == self.line:
                startItems.pop(0)
            endItems = self.items(self.line.line().p2())
            if len(endItems) and endItems[0] == self.line:
                endItems.pop(0)

            self.removeItem(self.line)
            self.line = None
            # проверка на соотвествие правил отрисовк
            if len(startItems) and len(endItems) and \
                    startItems[0] != endItems[0]:
                startItem = startItems[0]
                endItem = endItems[0]
                if self.myMode == self.InsertCommentLine:
                    arrow = CommentLine(startItem, endItem)
                elif self.myMode == self.InsertArrowAssociation:
                    arrow = ArrowAssociation(startItem,endItem)
                elif self.myMode == self.InsertArrowGeneralization:
                    arrow = ArrowGeneralization(startItem,endItem)
                if arrow.isValid():
                    arrow.setColor(self.myLineColor)
                    arrow.setZValue(-1000.0)
                    self.addItem(arrow)
                    startItem.addArrow(arrow)
                    endItem.addArrow(arrow)
                    arrow.updatePosition()
        self.line = None
        super(DiagramScene, self).mouseReleaseEvent(mouseEvent)

    def isItemChange(self, type):
        for item in self.selectedItems():
            if isinstance(item, type):
                return True
        return False


class MainWindow(QtGui.QMainWindow):
    InsertTextButton = 10

    def __init__(self):
        super(MainWindow, self).__init__()

        self.createActions()
        self.createMenus()
        self.scene = DiagramScene(self.itemMenu)
        self.scene.setSceneRect(QtCore.QRectF(0, 0, 5000, 5000))
        self.scene.itemInserted.connect(self.itemInserted)
        self.scene.textInserted.connect(self.textInserted)
        self.scene.itemSelected.connect(self.itemSelected)

        self.createToolbars()

        layout = QtGui.QHBoxLayout()
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing,True)
        layout.addWidget(self.view)

        self.widget = QtGui.QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Use case diagramm")
        self.scene.setMode(self.scene.InsertText)

    def deleteItem(self):
        for item in self.scene.selectedItems():
            if isinstance(item, ElementDiagramm):
				pass
                #item.removeArrows()
            self.scene.removeItem(item)

    def pointerGroupClicked(self, i):
        self.scene.setMode(self.pointerTypeGroup.checkedId())

    def bringToFront(self):
        if not scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() >= zValue and isinstance(item, ElementDiagramm)):
                zValue = item.zValue() + 0.1
        selectedItem.setZValue(zValue)

    def sendToBack(self):
        if not scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() <= zValue and isinstance(item, ElementDiagramm)):
                zValue = item.zValue() - 0.1
        selectedItem.setZValue(zValue)

    def itemInserted(self, item):
        self.pointerTypeGroup.button(DiagramScene.MoveItem).setChecked(True)
        self.scene.setMode(self.pointerTypeGroup.checkedId())

    def textInserted(self, item):
        pass

    def sceneScaleChanged(self, scale):
        newScale = int(scale[:-1]) / 100.0
        oldMatrix = self.view.matrix()
        self.view.resetMatrix()
        self.view.translate(oldMatrix.dx(), oldMatrix.dy())
        self.view.scale(newScale, newScale)

    def textButtonTriggered(self):
        self.scene.setTextColor(QtGui.QColor(self.textAction.data()))

    def fillButtonTriggered(self):
        self.scene.setItemColor(QtGui.QColor(self.fillAction.data()))

    def lineButtonTriggered(self):
        self.scene.setLineColor(QtGui.QColor(self.lineAction.data()))

    def itemSelected(self, item):
        pass
    def about(self):
        QtGui.QMessageBox.about(self, "About Diagram Scene",
                "The <b>Diagram Scene</b> example shows use of the graphics framework.")

    def createActions(self):
        
        self.arrowTotal = QtGui.QAction(
                QtGui.QIcon(':/images/linepointer.png'), "Arrow &Total",
                self,shortcut = "Ctrl+A",statusTip = "Arrow total",
                triggered = self.toArrowTotal
        )
        
        self.arrowComment = QtGui.QAction(
                QtGui.QIcon(':/images/linepointer.png'), "Arrow &Comment",
                self,shortcut = "Ctrl+A",statusTip = "Comment",
                triggered = self.toArrowComment
        )
        
        self.arrow = QtGui.QAction(
                QtGui.QIcon(':/images/linepointer.png'), "Arrowt",
                self,shortcut = "Ctrl+A",statusTip = "Arrow",
                triggered = self.toArrow
        )

        self.useCaseAction = QtGui.QAction(
                QtGui.QIcon(':/images/usecase.png'), "Use case",
                self,shortcut = "Ctrl+A",statusTip = "Use case",
                triggered = self.toUseCase
        )

        self.actorAction = QtGui.QAction(
                QtGui.QIcon(':/images/actor.png'), "Actor",
                self,shortcut = "Ctrl+A",statusTip = "Actor",
                triggered = self.toActor
        )
        self.commentAction = QtGui.QAction(
                QtGui.QIcon(':/images/comment.png'), "Actor",
                self,shortcut = "Ctrl+A",statusTip = "Actor",
                triggered = self.toComment
        )
        
        self.toFrontAction = QtGui.QAction(
                QtGui.QIcon(':/images/bringtofront.png'), "Bring to &Front",
                self, shortcut="Ctrl+F", statusTip="Bring item to front",
                triggered = self.bringToFront)
        
        self.sendBackAction = QtGui.QAction(
                QtGui.QIcon(':/images/sendtoback.png'), "Send to &Back", self,
                shortcut="Ctrl+B", statusTip="Send item to back",
                triggered=self.sendToBack)

        self.deleteAction = QtGui.QAction(QtGui.QIcon(':/images/delete.png'),
                "&Delete", self, shortcut="Delete",
                statusTip="Delete item from diagram",
                triggered=self.deleteItem)

        self.exitAction = QtGui.QAction("E&xit", self, shortcut="Ctrl+X",
                statusTip="Quit Scenediagram example", triggered=self.close)
        self.aboutAction = QtGui.QAction("A&bout", self, shortcut="Ctrl+B",
                triggered=self.about)

    def toArrowTotal(self):
        self.scene.setMode(self.scene.InsertArrowAssociation)

    def toArrowComment(self):
        self.scene.setMode(self.scene.InsertCommentLine)

    def toArrow(self):
        self.scene.setMode(self.scene.InsertArrowGeneralization)
    
    def toUseCase(self):
        self.scene.setMode(self.scene.InsertUseCase)
    
    def toActor(self):
        self.scene.setMode(self.scene.InsertActor)
    
    def toComment(self):
        self.scene.setMode(self.scene.InsertText)
    
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.exitAction)

        self.itemMenu = self.menuBar().addMenu("&Item")
        self.itemMenu.addAction(self.deleteAction)
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(self.toFrontAction)
        self.itemMenu.addAction(self.sendBackAction)

        self.aboutMenu = self.menuBar().addMenu("&Help")
        self.aboutMenu.addAction(self.aboutAction)

    def createToolbars(self):
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.deleteAction)
        self.editToolBar.addAction(self.toFrontAction)
        self.editToolBar.addAction(self.sendBackAction)
        self.editToolBar.addAction(self.arrow)
        self.editToolBar.addAction(self.arrowComment)
        self.editToolBar.addAction(self.arrowTotal)
        self.editToolBar.addAction(self.useCaseAction)
        self.editToolBar.addAction(self.actorAction)
        self.editToolBar.addAction(self.commentAction)


        pointerButton = QtGui.QToolButton()
        pointerButton.setCheckable(True)
        pointerButton.setChecked(True)
        pointerButton.setIcon(QtGui.QIcon(':/images/pointer.png'))
        linePointerButton = QtGui.QToolButton()
        linePointerButton.setCheckable(True)
        linePointerButton.setIcon(QtGui.QIcon(':/images/linepointer.png'))

        self.pointerTypeGroup = QtGui.QButtonGroup()
        self.pointerTypeGroup.addButton(pointerButton, DiagramScene.MoveItem)
        self.pointerTypeGroup.addButton(linePointerButton,
                DiagramScene.InsertLine)
        self.pointerTypeGroup.buttonClicked[int].connect(self.pointerGroupClicked)

        self.sceneScaleCombo = QtGui.QComboBox()
        self.sceneScaleCombo.addItems(["50%", "75%", "100%", "125%", "150%"])
        self.sceneScaleCombo.setCurrentIndex(2)
        self.sceneScaleCombo.currentIndexChanged[str].connect(self.sceneScaleChanged)

        self.pointerToolbar = self.addToolBar("Pointer type")
        self.pointerToolbar.addWidget(pointerButton)
        self.pointerToolbar.addWidget(linePointerButton)
        self.pointerToolbar.addWidget(self.sceneScaleCombo)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.show()

    sys.exit(app.exec_())
