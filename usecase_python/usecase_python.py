# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                       coding: UTF-8                     #
#     Dialite - программа для создания use case диаграмм  #
#          Авторы: студенты группы ИВТ-460 ВолгГТУ        #
#  Ли Е.В., Синицын А.А., Рашевский Н.М., Дмитриенко Д.В. #
#     http://code.google.com/p/usecasevstu/ (c) 2011      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from PySide import QtCore, QtGui
import math
import diagramscene_rc

# класс для элемента для хранение в файле
class ElementData:    
    def __init__(self,item=None):
        if item!=None:
            self.point = item.scenePos()
            self.id = item.getId()
            self.type = item.getType()
            if(isinstance(item,TotalLineDiagram)):
                self.idStart = item.startItem().getId()
                self.idEnd = item.endItem().getId()
            elif(isinstance(item,ElementDiagramm)):
                self.text = item.toPlainText()
            elif(isinstance(item,PictureElement)):
                self.fName = item.fileName
                
    def save(self,stream):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        stream.writeUInt32(self.type)
        stream.writeUInt32(self.id)
        stream = stream.__lshift__ (self.point)
        if(self.type == DiagramScene.CommentLineType or self.type == DiagramScene.ArrowAssociationType or \
           self.type == DiagramScene.ArrowGeneralizationType):
            stream.writeUInt32 (self.idStart)
            stream.writeUInt32 (self.idEnd)
        elif(self.type == DiagramScene.PictureType):
            stream.writeQString(self.fName)
        else:
            stream.writeQString (self.text)
        QtGui.QApplication.restoreOverrideCursor()
        return stream
    
    def read(self,stream):
        type = stream.readInt32()
        id = stream.readInt32()
        pos = QtCore.QPointF(0,0)
        stream = stream.__rshift__(pos)
        if type == DiagramScene.ActorType or type == DiagramScene.CommentType \
                or type == DiagramScene.UseCaseType:
            if type == DiagramScene.ActorType:
                item = Actor()
            elif type == DiagramScene.CommentType:
                item = Comment()
            elif type == DiagramScene.UseCaseType:
                item = UseCase()
            str = stream.readString()
            item.setPlainText(str)
        if type == DiagramScene.CommentLineType or type == DiagramScene.ArrowAssociationType \
                or type == DiagramScene.ArrowGeneralizationType:
            if type == DiagramScene.CommentLineType:
                item = CommentLine()
            elif type == DiagramScene.ArrowAssociationType:
                item = ArrowAssociation()
            elif type == DiagramScene.ArrowGeneralizationType:
                item = ArrowGeneralization()
            idStart = stream.readInt32()
            idEnd = stream.readInt32()
            item.setIdStart(idStart)
            item.setIdEnd(idEnd)
        if type == DiagramScene.PictureType:
            str = stream.readString()
            item = PictureElement(str)
        item.setId(id)
        item.setPos(pos)
        return item
    
    def getItem(self):
        if self.type == DiagramScene.ActorType or self.type == DiagramScene.CommentType \
                or self.type == DiagramScene.UseCaseType:
            if self.type == DiagramScene.ActorType:
                item = Actor()
            elif self.type == DiagramScene.CommentType:
                item = Comment()
            elif self.type == DiagramScene.UseCaseType:
                item = UseCase()
            item.setPlainText(self.text)
        if self.type == DiagramScene.CommentLineType or self.type == DiagramScene.ArrowAssociationType \
                or self.type == DiagramScene.ArrowGeneralizationType:
            if self.type == DiagramScene.CommentLineType:
                item = CommentLine()
            elif self.type == DiagramScene.ArrowAssociationType:
                item = ArrowAssociation()
            elif self.type == DiagramScene.ArrowGeneralizationType:
                item = ArrowGeneralization()
            item.setIdStart(self.idStart)
            item.setIdEnd(self.idEnd)
        if self.type == DiagramScene.PictureType:
            item = PictureElement(self.fName)
        item.setId(self.id)
        item.setPos(self.point)
        return item
            
def getPoints(self, startItem, endItem):

    calcType = 4

    if type(startItem) == UseCase and type(endItem) == UseCase:
        calcType = 1
        startPoint = self.mapFromItem(startItem, startItem.wideRect().center())
        endPoint = self.mapFromItem(endItem, endItem.wideRect().center())
        width1 = startItem.wideRect().width()
        width2 = endItem.wideRect().width()
        height1 = startItem.wideRect().height()
        height2 = endItem.wideRect().height()


    if type(startItem) == UseCase and (type(endItem) == Comment or type(endItem) == Actor):
        calcType = 2
        startPoint = self.mapFromItem(startItem, startItem.wideRect().center())
        endPoint = self.mapFromItem(endItem, endItem.boundingRect().center())
        width1 = startItem.wideRect().width()
        width2 = endItem.boundingRect().width()
        height1 = startItem.wideRect().height()
        height2 = endItem.boundingRect().height()

    if (type(startItem) == Comment or type(startItem) == Actor) and type(endItem) == UseCase:
        calcType = 3
        startPoint = self.mapFromItem(startItem, startItem.boundingRect().center())
        endPoint = self.mapFromItem(endItem, endItem.wideRect().center())
        width1 = startItem.boundingRect().width()
        width2 = endItem.wideRect().width()
        height1 = startItem.boundingRect().height()
        height2 = endItem.wideRect().height()

    if (type(startItem) == Comment or type(startItem) == Actor) and (type(endItem) == Comment or type(endItem) == Actor):
        calcType = 4
        startPoint = self.mapFromItem(startItem, startItem.boundingRect().center())
        endPoint = self.mapFromItem(endItem, endItem.boundingRect().center())
        width1 = startItem.boundingRect().width()
        width2 = endItem.boundingRect().width()
        height1 = startItem.boundingRect().height()
        height2 = endItem.boundingRect().height()
    

    result = [QtCore.QPointF(0,0), QtCore.QPointF(0,0)]

    calc11 = LineCircleCalculation(startPoint, endPoint, width1, height1)
    calc12 = LineCircleCalculation(endPoint, startPoint, width2, height2)
    calc21 = LineCircleCalculation(startPoint, endPoint, width1, height1)
    calc22 = LineRectCalculation(endPoint, startPoint, width2, height2)
    calc31 = LineRectCalculation(startPoint, endPoint, width1, height1)
    calc32 = LineCircleCalculation(endPoint, startPoint, width2, height2)
    calc41 = LineRectCalculation(startPoint, endPoint, width1, height1)
    calc42 = LineRectCalculation(endPoint, startPoint, width2, height2)

    if calcType == 1:

        #circle-circle
        result[0] = calc11.getResult()
        result[1] = calc12.getResult()

    if calcType == 2:
        #circle-rect
        result[0] = calc21.getResult()
        result[1] = calc22.getResult()

    if calcType == 3:
        #rect-circle
        result[0] = calc31.getResult()
        result[1] = calc32.getResult()

    if calcType == 4:
        #rect-rect
        result[0] = calc41.getResult()
        result[1] = calc42.getResult()

    return result

class LineCircleCalculation:

    def __init__(self, circleCenter, outerPoint, circleWidth, circleHeight):

        self.x1 = circleCenter.x()
        self.y1 = circleCenter.y()
        self.x3 = outerPoint.x()
        self.y3 = outerPoint.y()
        self.w = circleWidth
        self.h = circleHeight
        self.isVerticalLine = False
        self.isHorizontalLine = False
        self.dx = 0
        self.dy = 0
        self.r = math.sqrt((self.y3-self.y1)*(self.y3-self.y1) + (self.x3-self.x1)*(self.x3-self.x1))
        if self.x3-self.x1 == 0:
            self.isVerticalLine = True
        elif self.y3-self.y1 == 0:
            self.isHorizontalLine = True
        else:
            self.line_k = abs(self.y3-self.y1)/abs(self.x3-self.x1)
            self.line_b = self.y1 - self.x1*(self.y3-self.y1)/(self.x3-self.x1)

    def getResult(self):

        res_x = self.x1
        res_y = self.y1
        if self.isVerticalLine:
            self.dx = 0
            self.dy = self.h/2
            if self.y3 > self.y1:
                res_y = self.y1 + self.h/2
            else:
                res_y = self.y1 - self.h/2
        elif self.isHorizontalLine:
            self.dx = self.w/2
            self.dy = 0
            if self.x3 > self.x1:
                res_x = self.x1 + self.w/2
            else:
                res_x = self.x1 - self.w/2
        else:
            angle = math.atan(self.line_k)
            self.dy = self.h/2*math.sin(angle)
            self.dx = self.w/2*math.cos(angle)

        if self.y3-self.y1>0 and self.x3-self.x1>0:
            res_x = self.x1 + self.dx
            res_y = self.y1 + self.dy
        elif self.y3-self.y1>0 and self.x3-self.x1<0:
            res_x = self.x1 - self.dx
            res_y = self.y1 + self.dy
        elif self.y3-self.y1<0 and self.x3-self.x1<0:
            res_x = self.x1 - self.dx
            res_y = self.y1 - self.dy
        elif self.y3-self.y1<0 and self.x3-self.x1>0:
            res_x = self.x1 + self.dx
            res_y = self.y1 - self.dy


        res = QtCore.QPointF(res_x, res_y)

        return res

class LineRectCalculation:

    def __init__(self, circleCenter, outerPoint, circleWidth, circleHeight):

        self.x1 = circleCenter.x()
        self.y1 = circleCenter.y()
        self.x3 = outerPoint.x()
        self.y3 = outerPoint.y()
        self.w = circleWidth
        self.h = circleHeight
        self.isVerticalLine = False
        self.isHorizontalLine = False
        self.dx = 0
        self.dy = 0
        self.r = math.sqrt((self.y3-self.y1)*(self.y3-self.y1) + (self.x3-self.x1)*(self.x3-self.x1))
        if self.x3-self.x1 == 0:
            self.isVerticalLine = True
        elif self.y3-self.y1 == 0:
            self.isHorizontalLine = True
        else:
            self.line_k = abs(self.y3-self.y1)/abs(self.x3-self.x1)
            self.line_b = self.y1 - self.x1*(self.y3-self.y1)/(self.x3-self.x1)

    def getResult(self):
        res_y = self.y1
        res_x = self.x1
        if self.isVerticalLine:
            self.dx = 0
            self.dy = self.h/2
            if self.y3 > self.y1:
                res_y = self.y1 + self.h/2
            else:
                res_y = self.y1 - self.h/2
        elif self.isHorizontalLine:
            self.dx = self.w/2
            self.dy = 0
            if self.x3 > self.x1:
                res_x = self.x1 + self.w/2
            else:
                res_x = self.x1 - self.w/2
        else:
            angle = math.atan(self.line_k)
            if angle < math.atan(self.h/self.w):
                self.dy = abs(self.y3-self.y1)*self.w/(2*self.r*math.cos(angle))#self.h/2*math.sin(angle)#
                self.dx = self.w/2
            if angle >= math.atan(self.h/self.w):
                self.dy = self.h/2
                self.dx = self.r*math.cos(angle)*self.h/(2*abs(self.y3-self.y1))#self.w/2*math.cos(angle)#
        if self.y3-self.y1>0 and self.x3-self.x1>0:
            res_x = self.x1 + self.dx
            res_y = self.y1 + self.dy
        elif self.y3-self.y1>0 and self.x3-self.x1<0:
            res_x = self.x1 - self.dx
            res_y = self.y1 + self.dy
        elif self.y3-self.y1<0 and self.x3-self.x1<0:
            res_x = self.x1 - self.dx
            res_y = self.y1 - self.dy
        elif self.y3-self.y1<0 and self.x3-self.x1>0:
            res_x = self.x1 + self.dx
            res_y = self.y1 - self.dy


        res = QtCore.QPointF(res_x, res_y)

        return res
# базовый класс для класса с картинкой
class PictureElement(QtGui.QGraphicsPixmapItem):
    selectedChange = QtCore.Signal(QtGui.QGraphicsItem)
    def __init__(self,fName,parent = None,scene=None):
        super(PictureElement, self).__init__(parent, scene)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable,True)
        self.type = DiagramScene.PictureType
        self.id = -1
        self.setNewPicture(fName)
    
    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            pass
        return value
        
    def setId(self,idN):
        self.id = idN
        
    def getId(self):
        return self.id
    
    def getType(self):
        return self.type
    
    def setNewPicture(self,string):
        self.fileName = string
        pixmap = QtGui.QPixmap(self.fileName,'PNG')
        self.setPixmap(pixmap)
        self.update()
    
# базовый класс для линии
class TotalLineDiagram(QtGui.QGraphicsLineItem):
    # типы линий
    def __init__(self, startItem=None, endItem=None, parent=None, scene=None):
         super(TotalLineDiagram, self).__init__(parent, scene)
         self.myStartItem = startItem
         self.myEndItem = endItem
         self.idStart = -1
         self.idEnd = -1
         self.arrowHead = QtGui.QPolygonF()

         self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
         self.myColor = QtCore.Qt.black
         self.setPen(QtGui.QPen(self.myColor, 2, QtCore.Qt.SolidLine,
               QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
         self.arrows = []
         self.id = -1
         self.type = DiagramScene.NonType
         self.doCopy = True
    def boundingRect(self):
        extra = (self.pen().width() + 20) / 2.0
        p1 = self.line().p1()
        p2 = self.line().p2()
        return QtCore.QRectF(p1, QtCore.QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def setId(self,idN):
        self.id = idN
        
    def getId(self):
        return self.id
    
    def setIdStart(self,id):
        self.idStart = id
        
    def setIdEnd(self,id):
        self.idEnd = id
        
    def getIdStart(self):
        return self.idStart
        
    def getIdEnd(self):
        return self.idEnd   
        
    def getType(self):
        return self.type
    
    def setColor(self, color):
        self.myColor = color

    def startItem(self):
        return self.myStartItem

    def endItem(self):
        return self.myEndItem
    
    def setStartItem(self,item):
        self.myStartItem = item
        
    def setEndItem(self,item):
        self.myEndItem = item
        
    def selection(self):
        angle = math.acos(self.line().dx() / self.line().length())
        size = 17
        if self.line().dy() >= 0:
            angle = (math.pi * 2) - angle
        p1 = self.line().p1() - QtCore.QPointF(math.sin(angle + math.pi / 3) * size, math.cos(angle + math.pi / 3) * size)
        p2 = self.line().p1() - QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3) * size, math.cos(angle + math.pi - math.pi / 3) * size)
        p3 = self.line().p2() + QtCore.QPointF(math.sin(angle + math.pi / 3) * size, math.cos(angle + math.pi / 3) * size)
        p4 = self.line().p2() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3) * size, math.cos(angle + math.pi - math.pi / 3) * size)
        p = QtGui.QPolygonF()
        p.push_back(p1)
        p.push_back(p2)
        p.push_back(p3)
        p.push_back(p4)
        p.push_back(p1)
        return p

    def shape(self):
        path = super(TotalLineDiagram, self).shape()
        path.addPolygon(self.arrowHead)
        path.addPolygon(self.selection())
        return path
        
    def updatePosition(self):
        line = QtCore.QLineF(self.mapFromItem(self.myStartItem, 0, 0), self.mapFromItem(self.myEndItem, 0, 0))
        self.setLine(line)
    # функция которую надо описать для дочеррних классов
    # определяет для начала и конца стрелки нужно ли её рисовать
    # return true - если нужно, false - если не нужно отрисовывать
    def isValid(self):
        count = 0
        for itemStart in self.startItem().arrows:
            for itemEnd in self.endItem().arrows:
                if itemStart == itemEnd:
                    count = count + 1
                    if count == 1:
                        return False
        return True
    def polygon(self):
        return QtGui.QPolygonF(self.boundingRect())

    def addArrow(self,item):
        self.arrows.append(item)

    def removeArrow(self,arrow):
        try:
            self.arrows.remove(arrow)
        except ValueError:
            pass
         
    def removeArrows(self):
        for arrow in self.arrows[:]:
            arrow.startItem().removeArrow(arrow)
            arrow.endItem().removeArrow(arrow)
            self.scene().removeItem(arrow)
    def startAndEndSelected(self):
        if self.startItem().isSelected() and self.endItem().isSelected():
            return True
        else: return False        
        
# клас для отрисовки линии комментария
class CommentLine(TotalLineDiagram):
    def __init__(self, startItem=None, endItem=None, parent=None, scene=None):
        super(CommentLine,self).__init__(startItem,endItem,parent,scene)
        self.type = DiagramScene.CommentLineType

    def isValid(self):
        if(((isinstance(self.startItem(),Comment) and \
            isinstance(self.endItem(), TotalLineDiagram))) or \
            ((isinstance(self.startItem(), TotalLineDiagram) and \
            isinstance(self.endItem(), Comment)))):
            return super(CommentLine,self).isValid()
        else: return False

    def paint(self, painter, option, widget=None):
        if self.myStartItem.collidesWithItem(self.myEndItem):
            return

        if isinstance(self.startItem(),TotalLineDiagram) and isinstance(self.endItem(), Comment):
           myStartItem = self.myEndItem
           myEndItem = self.myStartItem
        else: 
            myStartItem = self.myStartItem
            myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        # отрисовка пунктиром
        myPen.setStyle(QtCore.Qt.DotLine)
        myPen.setColor(self.myColor)
        # arrowSize = 20.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        points = [QtCore.QPointF(0,0), QtCore.QPointF(0,0)]
        if type(myStartItem) == Comment:
            param1 = self.mapFromItem(myStartItem, myStartItem.boundingRect().center())
            param2 = self.mapFromItem(myEndItem, myEndItem.boundingRect().center())
            param4 = myStartItem.boundingRect().height()
            param3 = myStartItem.boundingRect().width()
            points[1] = param2
        if type(myEndItem) == Comment :
            param1 = self.mapFromItem(myEndItem, myEndItem.boundingRect().center())
            param2 = self.mapFromItem(myStartItem, myStartItem.boundingRect().center())
            param4 = myEndItem.boundingRect().height()
            param3 = myEndItem.boundingRect().width()
            points[1] = param2

        calc = LineRectCalculation(param1, param2, param3, param4)
        points[0] = calc.getResult()
        centerLine = QtCore.QLineF(points[1], points[0])#centerLine = QtCore.QLineF(myStartItem.pos(), myEndItem.pos())
        
        self.setLine(centerLine)#QtCore.QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()

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

# клас для стрелки агрегации (с ромбом)
class ArrowAgregation(TotalLineDiagram):
    def __init__(self, startItem=None, endItem=None, parent=None, scene=None):
        super(ArrowAgregation,self).__init__(startItem,endItem,parent,scene)
        self.type = DiagramScene.ArrowAgregationType

    def isValid(self):
        if(((isinstance(self.startItem(),UseCase) and \
            isinstance(self.endItem(), UseCase))) or \
            ((isinstance(self.startItem(), Actor) and \
            isinstance(self.endItem(), Actor)))):
            return super(ArrowAgregation,self).isValid()
        else: return False

    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return

        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        myPen.setColor(self.myColor)
        arrowSize = 10.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        
        points = getPoints(self, myStartItem, myEndItem)

        centerLine = QtCore.QLineF(points[1], points[0])

        self.setLine(centerLine)#QtCore.QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrowP1 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)
        arrowP3 = arrowP1 + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)

        arrowP4 = arrowP2 + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        
        self.arrowHead.clear()
        
        painter.drawLine(line)
        #painter.drawLine(QtCore.QLineF(line.p1(), arrowP1))
        #painter.drawLine(QtCore.QLineF(line.p1(), arrowP2))
        #painter.drawLine(QtCore.QLineF(arrowP1, arrowP3))
        #painter.drawLine(QtCore.QLineF(arrowP2, arrowP4))
        
        for point in [line.p1(), arrowP1, arrowP3, arrowP4, arrowP2, line.p1()]:
            self.arrowHead.append(point)
        painter.setBrush(QtCore.Qt.white)
        #painter.drawLine(line)
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
         
    def copy(self):
        new = ArrowAgregation()
        return new
         
# клас для отрисовки линии include
class ArrowInclude(TotalLineDiagram):
    def __init__(self, startItem=None, endItem=None, parent=None, scene=None):
        super(ArrowInclude,self).__init__(startItem,endItem,parent,scene)
        self.type = DiagramScene.ArrowIncludeType

    def isValid(self):
        if(((isinstance(self.startItem(),UseCase) and \
            isinstance(self.endItem(), UseCase))) or \
            ((isinstance(self.startItem(), Actor) and \
            isinstance(self.endItem(), Actor)))):
            return super(ArrowInclude,self).isValid()
        else: return False

    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return

        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        myPen.setColor(self.myColor)
        arrowSize = 7.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        points = getPoints(self, myStartItem, myEndItem)

        centerLine = QtCore.QLineF(points[1], points[0])

        self.setLine(centerLine)#QtCore.QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrowP1 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)

        self.arrowHead.clear()
        painter.drawLine(QtCore.QLineF(line.p1(), arrowP1))
        painter.drawLine(QtCore.QLineF(line.p1(), arrowP2))
        myPen.setStyle(QtCore.Qt.DotLine)
        painter.setPen(myPen)
        painter.drawLine(line)
        
        lineText = "<< include >>"
        line2 = QtCore.QLineF(line)
        line2.setLength(line2.length()/2.0)
        centerPoint = line2.p2()
        centerPoint.setX(centerPoint.x() - len(lineText)*3)
        if angle>= 2*math.pi*7.0/8.0 or angle <= math.pi/6 or angle<=math.pi*8.0/7.0 and angle>=math.pi*7.0/8.0:
            centerPoint.setY(centerPoint.y()  - 7)
                
        painter.drawText(centerPoint, lineText)#QtCore.QPointF(line.p1().x() + line.dx()/2.0, line.p1().y() - line.dy()/2.0), lineText)
        
        
        
        if self.isSelected():
            painter.setPen(QtGui.QPen(myColor, 1, QtCore.Qt.DashLine))
            myLine = QtCore.QLineF(line)
            myLine.translate(0, 4.0)
            painter.drawLine(myLine)
            myLine.translate(0,-8.0)
            painter.drawLine(myLine)

    def polygon(self):
         return QtGui.QPolygonF(self.boundingRect())
     
    def copy(self):
        new = ArrowInclude()
        return new         
         

# класс для отрисовки стрелки ассоциации
class ArrowAssociation(TotalLineDiagram):
    def __init__(self, startItem=None, endItem=None, parent=None, scene=None):
        super(ArrowAssociation,self).__init__(startItem,endItem,parent,scene)
        self.type = DiagramScene.ArrowAssociationType

    def isValid(self):
        if((isinstance(self.startItem(),Actor) and \
            isinstance(self.endItem(), UseCase)) or \
            (isinstance(self.startItem(), UseCase) and \
            isinstance(self.endItem(), Actor))):
            return super(ArrowAssociation,self).isValid()
        elif ((isinstance(self.startItem(),Actor) and \
            isinstance(self.endItem(), Actor))):
            return super(ArrowAssociation,self).isValid()
        elif ((isinstance(self.startItem(),UseCase) and \
            isinstance(self.endItem(), UseCase))):
            return super(ArrowAssociation,self).isValid()
        else: return False

    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return

        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        myPen.setColor(self.myColor)
        arrowSize = 7.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        points = getPoints(self, myStartItem, myEndItem)

        centerLine = QtCore.QLineF(points[1], points[0])

        self.setLine(centerLine)#QtCore.QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrowP1 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)

        self.arrowHead.clear()
        
        painter.drawLine(line)
        painter.drawLine(QtCore.QLineF(line.p1(), arrowP1))
        painter.drawLine(QtCore.QLineF(line.p1(), arrowP2))
        if self.isSelected():
            painter.setPen(QtGui.QPen(myColor, 1, QtCore.Qt.DashLine))
            myLine = QtCore.QLineF(line)
            myLine.translate(0, 4.0)
            painter.drawLine(myLine)
            myLine.translate(0,-8.0)
            painter.drawLine(myLine)
            
    def polygon(self):
         return QtGui.QPolygonF(self.boundingRect())
     
    def copy(self):
        new = ArrowAssociation()
        return new

# клас для отрисовки линии extend
class ArrowExtend(TotalLineDiagram):
    def __init__(self, startItem=None, endItem=None, parent=None, scene=None):
        super(ArrowExtend,self).__init__(startItem,endItem,parent,scene)
        self.type = DiagramScene.ArrowExtendType

    def isValid(self):
        if(((isinstance(self.startItem(),UseCase) and \
            isinstance(self.endItem(), UseCase))) or \
            ((isinstance(self.startItem(), Actor) and \
            isinstance(self.endItem(), Actor)))):
            return super(ArrowExtend,self).isValid()
        else: return False

    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return

        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        myPen.setColor(self.myColor)
        arrowSize = 7.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        points = getPoints(self, myStartItem, myEndItem)

        centerLine = QtCore.QLineF(points[1], points[0])

        self.setLine(centerLine)#QtCore.QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrowP1 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)

        self.arrowHead.clear()
        painter.drawLine(QtCore.QLineF(line.p1(), arrowP1))
        painter.drawLine(QtCore.QLineF(line.p1(), arrowP2))
        myPen.setStyle(QtCore.Qt.DotLine)
        painter.setPen(myPen)
        painter.drawLine(line)
        
        lineText = "<< extend >>"
        line2 = QtCore.QLineF(line)
        line2.setLength(line2.length()/2.0)
        centerPoint = line2.p2()
        centerPoint.setX(centerPoint.x() - len(lineText)*3)
        if angle>= 2*math.pi*7.0/8.0 or angle <= math.pi/6 or angle<=math.pi*8.0/7.0 and angle>=math.pi*7.0/8.0:
            centerPoint.setY(centerPoint.y()  - 7)
                
        painter.drawText(centerPoint, lineText)#QtCore.QPointF(line.p1().x() + line.dx()/2.0, line.p1().y() - line.dy()/2.0), lineText)
        
        
        
        if self.isSelected():
            painter.setPen(QtGui.QPen(myColor, 1, QtCore.Qt.DashLine))
            myLine = QtCore.QLineF(line)
            myLine.translate(0, 4.0)
            painter.drawLine(myLine)
            myLine.translate(0,-8.0)
            painter.drawLine(myLine)

    def polygon(self):
         return QtGui.QPolygonF(self.boundingRect())
    def copy(self):
        new = ArrowExtend()
        return new 
        
# класс для отрисовки стрелки обобщения
class ArrowGeneralization(TotalLineDiagram):
    def __init__(self, startItem=None, endItem=None, parent=None, scene=None):
        super(ArrowGeneralization,self).__init__(startItem,endItem,parent,scene)
        self.type = DiagramScene.ArrowGeneralizationType

    def isValid(self):
        if ((isinstance(self.startItem(),Actor) and \
            isinstance(self.endItem(), Actor)) or \
            (isinstance(self.startItem(), UseCase) and \
            isinstance(self.endItem(), UseCase))):
            return super(ArrowGeneralization,self).isValid()
        else: return False
    
    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return

        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        myPen.setColor(self.myColor)
        arrowSize = 7.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        points = getPoints(self, myStartItem, myEndItem)

        centerLine = QtCore.QLineF(points[1], points[0])


        self.setLine(centerLine)#QtCore.QLineF(intersectPoint, myStartItem.pos()))
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
        painter.setBrush(QtCore.Qt.white)
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
    def copy(self):
        new = ArrowGeneralization()
        return new

class ElementDiagramm(QtGui.QGraphicsTextItem):

    lostFocus = QtCore.Signal(QtGui.QGraphicsTextItem)

    selectedChange = QtCore.Signal(QtGui.QGraphicsItem)
    
    diagramChanged = QtCore.Signal()
    
    def __init__(self, parent=None, scene=None):
        super(ElementDiagramm, self).__init__(parent, scene)
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.myTypeElement = DiagramScene.NonType
        self.arrows = []
        self.id = -1
        self.doCopy = True
    def countArrows(self):
        print self.arrows
        
    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            for i in self.arrows:
                i.update()
            # self.selectedChange.emit(self)
        return value
    
    def setId(self,id):
        self.id = id
        
    def getId(self):
        return self.id
    
    def focusInEvent(self, event):
        self.prevStr = self.toPlainText()
    
    def focusOutEvent(self, event):
        if self.myTypeElement==DiagramScene.UseCaseType or self.myTypeElement==DiagramScene.CommentType:
            #
            string=self.toPlainText()
            string=string.encode("UTF-8")
            i=0
            #ищем и удаляем пробелы в строке справа
            while len(string)>i and string[i]==' ':
                i+=1
            if i!=0:    
                string=string[i-1:]
            i=len(string)-1
            #ищем и удаляем пробелы в строке слева
            while i>0 and string[i]==' ':
                i-=1
            if i!=len(string)-1:    
                string=string[:i+1]
            #выравниваем по центру, если длина меньше 15, то бобавляем пробелы слева и справа
            #string=string.center(15)
            self.setPlainText(string)
            
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.lostFocus.emit(self)
        
        super(ElementDiagramm, self).focusOutEvent(event)
        
        if(self.prevStr != self.toPlainText()):
            self.diagramChanged.emit()
    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == QtCore.Qt.NoTextInteraction:
            self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        super(ElementDiagramm, self).mouseDoubleClickEvent(event)
        
    def getType(self):
        return self.myTypeElement

    def polygon(self):
        return QtGui.QPolygonF(self.boundingRect())

    def addArrow(self,item):
        self.arrows.append(item)

    def removeArrow(self,arrow):
        try:
            self.arrows.remove(arrow)
        except ValueError:
            pass
         
    def removeArrows(self):
        for arrow in self.arrows[:]:
            arrow.removeArrows()
            arrow.startItem().removeArrow(arrow)
            arrow.endItem().removeArrow(arrow)
            self.scene().removeItem(arrow)
            
class Comment(ElementDiagramm):
    def __init__(self, parent=None, scene=None):
        super(Comment, self).__init__(parent, scene)
        self.myTypeElement = DiagramScene.CommentType
        string=""
        string=string.center(20)
        self.setPlainText(string)

    def paint(self, painter, option, widget=None):
        bodyRect = self.boundingRect()
        pointStart =  QtCore.QPointF((bodyRect.topRight().x()- bodyRect.topLeft().x())*9.0/10.0,
            bodyRect.topLeft().y());
        pointEnd = QtCore.QPointF(bodyRect.topRight().x(),
            (bodyRect.bottomRight().y() - bodyRect.topRight().y())*1.0/10.0)

        linearGrad = QtGui.QLinearGradient(pointEnd, bodyRect.bottomLeft())

        linearGrad.setColorAt(0, QtCore.Qt.white)
        linearGrad.setColorAt(1, QtGui.QColor(255,255,255))
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
    def copy(self):
        new = Comment()
        new.setPlainText(self.toPlainText())
        return new

class UseCase(ElementDiagramm):
    def __init__(self, parent=None, scene=None):
        super(UseCase, self).__init__(parent, scene)
        self.myTypeElement = DiagramScene.UseCaseType
        string=""
        #string=string.center(20)
        self.setPlainText(string)
        
    # доделать для вида по умолчанию 
    def boundingRect(self):
        body = super(UseCase,self).boundingRect()
        return body
    
    def wideRect (self):
        bodyRect = self.boundingRect()
        #изменяем bodyrect, чтобы овал отрисовывался вокруг текста
        h = bodyRect.height()
        w = bodyRect.width()
        if w < 40:
            w = 40
        center = bodyRect.center()
        angle = math.atan(h/w)
        w1 = w*math.sqrt(2)
        h1 = h*math.sqrt(2)
        p1 = QtCore.QPointF(center.x() - w1/2, center.y() - h1/2)
        p2 = QtCore.QPointF(center.x() + w1/2, center.y() + h1/2)
        newBodyRect = QtCore.QRectF(p1,p2)
        return newBodyRect
        
    def paint(self, painter, option, widget=None):
        bodyRect = self.boundingRect()
        painter.drawEllipse(bodyRect)
        listCoord = bodyRect.getCoords()
        x1 = listCoord[0]
        y1 = listCoord[1]
        grad = QtGui.QRadialGradient(QtCore.QPointF(x1,y1),bodyRect.width())
        grad.setColorAt(1,QtGui.QColor(255,255,255))
        grad.setColorAt(0.5,QtCore.Qt.white)
        grad.setColorAt(0,QtCore.Qt.white)
        _path = QtGui.QPainterPath()
        #изменяем bodyrect, чтобы овал отрисовывался вокруг текста
        h = bodyRect.height()
        w = bodyRect.width()
        if w < 40:
            w = 40
        center = bodyRect.center()
        angle = math.atan(h/w)
        w1 = w*math.sqrt(2)
        h1 = h*math.sqrt(2)
        p1 = QtCore.QPointF(center.x() - w1/2, center.y() - h1/2)
        p2 = QtCore.QPointF(center.x() + w1/2, center.y() + h1/2)
        newBodyRect = QtCore.QRectF(p1,p2)
        _path.addEllipse(newBodyRect)
        painter.drawEllipse(newBodyRect)
        painter.fillPath(_path,QtGui.QBrush(grad))
        super(UseCase, self).paint(painter, option, widget)
    def polygon(self):
        return QtGui.QPolygonF(self.boundingRect())
    def copy(self):
        new = UseCase()
        new.setPlainText(self.toPlainText())
        return new
class Actor(ElementDiagramm):
    actorChanged = QtCore.Signal()
          
    def __init__(self, parent=None, scene=None):
        super(Actor, self).__init__(parent, scene)
        self.myTypeElement = DiagramScene.ActorType
        self.setTextWidth(65);
        self.setHtml("<img src=\":/images/actor1.png\" /><p align=\"center\">Actor</p>");
        textcursor=self.textCursor()
        textcursor.movePosition(QtGui.QTextCursor.Down,QtGui.QTextCursor.MoveAnchor,1)
        textcursor.movePosition(QtGui.QTextCursor.EndOfLine,QtGui.QTextCursor.KeepAnchor,5)
        self.setTextCursor(textcursor)
         
    def paint(self, painter, option, widget=None):
        super(Actor, self).paint(painter, option, widget)
    def polygon(self):
        return QtGui.QPolygonF(self.boundingRect())
    def focusOutEvent(self, event):
        if(self.prevStr != self.toPlainText()):
            self.actorChanged.emit()            
        string=self.toPlainText()
        string=string.encode("UTF-8")
        imgFlag=False
        pos=0
        i=0
        #пока не конец строки и картинка не найдена
        while i<len(string) and imgFlag!=True:
            #код проверяемого символа, больше допустимого
            if ord(string[i])>127:
                imgFlag=True
                pos=i
            i += 1
        #если картинка не найдена вставляем ее в начало
        if imgFlag==False:
            self.setHtml("<img src=\":/images/actor1.png\" /><p align=\"center\">"+string+"</p>")
        #если картинка найдена
        if imgFlag==True and (pos-1)!=0:
            #если картинка без текста
            if len(string)-pos-4<=0:
                self.setHtml("<img src=\":/images/actor1.png\" /><p align=\"center\">Actor</p>");
            else:
                self.setHtml("<img src=\":/images/actor1.png\" /><p align=\"center\">"+string[pos+4:]+"</p>")
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)        
        self.lostFocus.emit(self)
    def copy(self):
        new = Actor()
        new.setPlainText(self.toPlainText())
        return new
            
class DiagramScene(QtGui.QGraphicsScene):
   
    PictureType,ArrowGeneralizationType,ArrowIncludeType,ArrowExtendType,ArrowAgregationType,CommentLineType, ArrowAssociationType,NonType,CommentType,UseCaseType,ActorType,InsertItem, InsertLine, InsertText, MoveItem,InsertCommentLine,InsertUseCase,InsertArrowAssociation,InsertArrowGeneralization,InsertArrowInclude,InsertArrowExtend,InsertArrowAgregation,InsertActor,InsertPicture  = range(24)

    itemInserted = QtCore.Signal(ElementDiagramm)

    textInserted = QtCore.Signal(QtGui.QGraphicsTextItem)

    itemSelected = QtCore.Signal(QtGui.QGraphicsItem)
    textEndInserted = QtCore.Signal()
    diagramChanged = QtCore.Signal()

    elements = []
    Arrows = []
    pictures = []
    Id = 0
    changeFlag = False
    curMouseCoord = QtCore.QPointF(0,0)
    #высота рабочей области
    heightWorkPlace = 1000.0
    #ширина рабочей области
    widthWorkPlace = 2000.0
    def __init__(self, itemMenu, parent=None):
        super(DiagramScene, self).__init__(parent)

        self.myItemMenu = itemMenu
        self.myMode = self.MoveItem
        self.line = None
        self.textItem = None
        self.myItemColor = QtCore.Qt.white
        self.myTextColor = QtCore.Qt.black
        self.myLineColor = QtCore.Qt.black
        self.myFont = QtGui.QFont()
        self.picturePath = ""
        changeFlag=False
        self.doMove = True
        #self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(100,100,100,255)))
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
        self.update()
        
    def getElementsById(self,id):
        for item in self.elements:
            if item.getId() == id:
                return item
        for item in self.Arrows:
            if item.getId() == id:
                return item
        for item in self.pictures:
            if item.getId() == id:
                return item
        return None
    def checkPos (self,pos,height=0,width=0):
        currentPos=QtCore.QPointF()
        currentPos=pos
        flag=False
        if currentPos.y()>self.heightWorkPlace-height-1:
            flag=True
            currentPos.setY(self.heightWorkPlace-height)
        if currentPos.y()<0:
            flag=True
            currentPos.setY(0)
        if currentPos.x()>self.widthWorkPlace-width-1:
            flag=True
            currentPos.setX(self.widthWorkPlace-width)
        if currentPos.x()<0:
            flag=True
            currentPos.setX(0)
        return currentPos
        return flag
        #currentPos.
        
    def mousePressEvent(self, mouseEvent):
        self.pressed = True
        if (mouseEvent.button() != QtCore.Qt.LeftButton):
            self.curMouseCoord = mouseEvent.scenePos()
            pass
        if self.myMode == self.InsertArrowAssociation or self.myMode == self.InsertArrowGeneralization or self.myMode == self.InsertCommentLine or self.myMode == self.InsertArrowInclude or self.myMode == self.InsertArrowExtend or self.myMode == self.InsertArrowAgregation:
            self.line = QtGui.QGraphicsLineItem(QtCore.QLineF(mouseEvent.scenePos(),
                                        mouseEvent.scenePos()))
            self.line.setPen(QtGui.QPen(self.myLineColor, 2))
            self.addItem(self.line)
        elif self.myMode == self.InsertText:
            textItem = Comment()
            textItem.diagramChanged.connect(self.textElementChanged)
        elif self.myMode == self.InsertUseCase:
            textItem = UseCase()
            textItem.diagramChanged.connect(self.textElementChanged)
        elif self.myMode == self.InsertActor:
            textItem = Actor()
            textItem.actorChanged.connect(self.textElementChanged)
        if self.myMode == self.InsertText or self.myMode == self.InsertUseCase or \
           self.myMode == self.InsertActor:
            self.initTextItem(textItem, mouseEvent.scenePos())
        super(DiagramScene, self).mousePressEvent(mouseEvent)
        self.update()
        self.pressPos = mouseEvent.scenePos();
    def initTextItem(self,textItem,pos):
        textItem.setFont(self.myFont)
        textItem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        textItem.setZValue(1000.0)
        textItem.lostFocus.connect(self.editorLostFocus)
        textItem.selectedChange.connect(self.itemSelected)
        #if self.myMode == self.InsertActor:
         #   textItem.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.addItem(textItem)
        textItem.setDefaultTextColor(self.myTextColor)
        itemSize=QtCore.QRectF()
        itemSize = textItem.boundingRect()
        if isinstance(textItem,ElementDiagramm):
            textItem.setPos(self.checkPos(pos,itemSize.height(),itemSize.width()))
        # увеличиваем идентификатор
        self.Id = self.Id + 1
        textItem.setId(self.Id)
        self.elements.append(textItem)            
        self.diagramChanged.emit()
    def textElementChanged(self):
            self.diagramChanged.emit()
    
    def addPicture(self,fString):
        pic = PictureElement(fString)
        #pic.selectedChange.connect(self.itemSelected)
        pic.setPos(QtCore.QPointF(0,0))
        self.Id = self.Id+1
        pic.setId(self.Id)
        self.pictures.append(pic)
        self.addItem(pic)
        self.diagramChanged.emit()
    def mouseMoveEvent(self, mouseEvent):
        if self.pressed == True:
            if (self.myMode == self.InsertArrowAssociation or self.myMode == self.InsertArrowGeneralization or self.myMode == self.InsertCommentLine or self.myMode == self.InsertArrowInclude or self.myMode == self.InsertArrowExtend or self.myMode == self.InsertArrowAgregation)  and self.line :
                newLine = QtCore.QLineF(self.line.line().p1(), mouseEvent.scenePos())
                self.line.setLine(newLine)
            elif self.myMode == self.MoveItem:
                if mouseEvent.modifiers() == QtCore.Qt.AltModifier and self.doMove == True:   
                    itemsArrow,itemElement = self.processingSelectElement()
                    # сначало копируем все элементы
                    for arr in itemsArrow:
                        c = arr.copy()
                        c.setStartItem(itemElement[arr.startItem()])
                        c.setEndItem(itemElement[arr.endItem()])
                        self.initArrow(c)
                        self.addItem(c)
                        self.Arrows.append(c)
                        c.setSelected(False)
                        arr.setSelected(True)
                        c.updatePosition()
                        self.diagramChanged.emit()
                        self.doMove = False
                super(DiagramScene, self).mouseMoveEvent(mouseEvent)
            self.update()
    def processingSelectElement(self):
        itemsArrow = []
        itemElement =  {}
        for item in self.selectedItems():
            if isinstance(item, ElementDiagramm):
                c = item.copy()
                c.doCopy = False
                item.doCopy = False
                self.initTextItem(c, item.scenePos())
                item.setZValue(item.zValue()+1)
                c.setSelected(False)
                self.doMove = False
                for arr in item.arrows:
                    if arr.isSelected() == False or arr.startAndEndSelected() == False:
                        c.arrows.append(arr)
                        if arr.startItem() == item:
                            arr.setStartItem(c)
                        elif arr.endItem() == item:
                            arr.setEndItem(c)
                for arr in c.arrows:
                    item.arrows.remove(arr)
                itemElement.update({item:c})
            elif isinstance(item, TotalLineDiagram):
                if item.startItem().isSelected() and item.endItem().isSelected():
                    itemsArrow.append(item)
        return itemsArrow,itemElement
    def keyReleaseEvent (self, event):
        self.update()
        super(DiagramScene, self).keyReleaseEvent(event)
    def keyPressEvent (self, event):
        self.update()
        super(DiagramScene, self).keyReleaseEvent(event)
    def getElements(self):
        return self.elements
    
    def mouseReleaseEvent(self, mouseEvent):
        self.pressed = False
        if self.line and (self.myMode == self.InsertArrowAssociation or self.myMode == self.InsertArrowGeneralization or self.myMode == self.InsertCommentLine or self.myMode == self.InsertArrowInclude or self.myMode == self.InsertArrowExtend or self.myMode == self.InsertArrowAgregation):
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
                elif self.myMode == self.InsertArrowInclude:
                     arrow = ArrowInclude(startItem,endItem)
                elif self.myMode == self.InsertArrowExtend:
                     arrow = ArrowExtend(startItem,endItem)     
                elif self.myMode == self.InsertArrowAgregation:
                     arrow = ArrowAgregation(startItem,endItem)     
            
                if arrow.isValid():
                     self.initArrow(arrow)
                     self.addItem(arrow)
                     startItem.addArrow(arrow)
                     endItem.addArrow(arrow)
                     self.Arrows.append(arrow)
                     arrow.updatePosition()
                     self.diagramChanged.emit()
        else:
            curitems=self.items()
            itemSize=QtCore.QRectF()
            already = False
            for item in curitems:
                itemSize = item.boundingRect()
                if isinstance(item,ElementDiagramm)or isinstance(item,PictureElement):
                    if (already != True and self.myMode == 11 and self.pressPos != item.scenePos() and self.pressPos != mouseEvent.scenePos()): 
                        self.diagramChanged.emit()
                        already = True
                    item.setPos(self.checkPos(item.scenePos(),itemSize.height(),itemSize.width()))
                item.update()
                if isinstance(item,ElementDiagramm):
                    for arrow in item.arrows:
                        arrow.updatePosition()
        self.line = None
        #после добавления элемента, переходит в состояние перетаскивания
        self.myMode = self.MoveItem
        self.textEndInserted.emit()
        super(DiagramScene, self).mouseReleaseEvent(mouseEvent)
        if self.doMove == False:
            self.doMove = True
        self.update()
    def initArrow(self,arrow):
        self.Id = self.Id + 1
        arrow.setId(self.Id)
        arrow.setColor(self.myLineColor)
        arrow.setZValue(10.0)
    def isItemChange(self, type):
        for item in self.selectedItems():
            if isinstance(item, type):
                return True
        return False
    def getChangeFlag(self):
        return self.changeFlag
    def setChangeFlag(self,flag):
        self.changeFlag=flag

class MainWindow(QtGui.QMainWindow):
    currentFileName = ""
    undoStack = []
    currentState = 0
    coordPaste = QtCore.QPointF(0,0)

    def __init__(self):
        super(MainWindow, self).__init__()
                
        self.createActions()
        self.createMenus()
        self.scene = DiagramScene(self.itemMenu)
        self.scene.setSceneRect(QtCore.QRectF(0, 0, self.scene.widthWorkPlace, self.scene.heightWorkPlace))
        self.scene.addRect(0.0,0.0, self.scene.widthWorkPlace, self.scene.heightWorkPlace,QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)),4.0),QtGui.QBrush(QtGui.QColor(255,255,255,255)))
        self.scene.itemInserted.connect(self.itemInserted)
        self.scene.textInserted.connect(self.textInserted)
        self.scene.textEndInserted.connect(self.textEndInserted)
        self.scene.diagramChanged.connect(self.diagramChanged)
        self.scene.itemSelected.connect(self.itemSelected)
        self.createToolbars()

        layout = QtGui.QHBoxLayout()
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing,True)
        self.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.sceneContextMenu)
        
        layout.addWidget(self.view)
        
        self.widget = QtGui.QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle(unicode("UseCaseDiagram - Диаграмма","UTF-8"))
        self.setWindowIcon(QtGui.QIcon(':/images/program.png'))
        self.pointer.setChecked(True)
        QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("UTF-8"));
        
        self.saveScenesElements()
        
    def sceneContextMenu(self):
        menu = QtGui.QMenu(self)
        menu.addAction(self.cutAction)
        menu.addAction(self.copyAction)
        menu.addAction(self.pasteAction)
        menu.addSeparator()
        menu.addAction(self.deleteAction)
        qwe = len(self.scene.selectedItems())
        if len(self.scene.selectedItems()) != 0:
            self.cutAction.setEnabled(True)
            self.copyAction.setEnabled(True)
            self.deleteAction.setEnabled(True)
        else:
            self.cutAction.setEnabled(False)
            self.copyAction.setEnabled(False)
            self.deleteAction.setEnabled(False)
        self.coordPaste = self.scene.curMouseCoord
        menu.exec_(QtGui.QCursor.pos())
        self.cutAction.setEnabled(True)
        self.copyAction.setEnabled(True)
        self.deleteAction.setEnabled(True)
    def falseChecked(self):
        self.arrowTotal.setChecked(False)
        self.arrowComment.setChecked(False)
        self.arrow.setChecked(False)
        self.arrowInclude.setChecked(False)
        self.arrowExtend.setChecked(False)
        self.arrowAgregation.setChecked(False)
        self.useCaseAction.setChecked(False)
        self.commentAction.setChecked(False)
        self.actorAction.setChecked(False)
        self.picAction.setChecked(False)
        self.pointer.setChecked(False)
        
    def undo(self):
        self.scene.setChangeFlag(True)
        if(self.currentState > 1):
            self.currentState = self.currentState - 1
            self.redoAction.setEnabled(True)
            if(self.currentState == 1):
                self.undoAction.setEnabled(False)
                         
        self.showScenesElements(self.undoStack[self.currentState-1] )
        
    def redo(self):
        self.scene.setChangeFlag(True)
        if(self.currentState < len(self.undoStack)): 
            self.currentState = self.currentState + 1
            if(self.currentState == len(self.undoStack)):
                self.redoAction.setEnabled(False)
            if(self.currentState > 1):
                self.undoAction.setEnabled(True)
            
        self.showScenesElements(self.undoStack[self.currentState-1])
        
    def saveScenesElements(self):
        sceneElements = []
        
        elements = []
        pictures = []
        arraws = []
        
        for i in self.scene.getElements():
            elements.append(ElementData(i)) 
        for i in self.scene.pictures:
            pictures.append(ElementData(i))
        for i in self.scene.Arrows:
            arraws.append(ElementData(i))
            
        sceneElements.append(elements)
        sceneElements.append(pictures)
        sceneElements.append(arraws)
        sceneElements.append(self.scene.Id)
        
        i = self.currentState
        while(i < len(self.undoStack)):
            self.undoStack.pop()
        self.undoStack.append(sceneElements)
        
        self.currentState = len(self.undoStack)

        if(self.currentState == len(self.undoStack)):
            self.redoAction.setEnabled(False) 
        if(self.currentState > 1):
            self.undoAction.setEnabled(True)
        else:
            self.undoAction.setEnabled(False)

    def cleanScenesElements(self):
        for i in self.undoStack:
            self.undoStack.pop()
        self.currentState = 0

    def showScenesElements(self,sceneElements):
        self.clearAll()
        self.scene.addRect(0.0,0.0, self.scene.widthWorkPlace, self.scene.heightWorkPlace,QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)),4.0),QtGui.QBrush(QtGui.QColor(255,255,255,255)))

        elements = sceneElements[0]
        pictures = sceneElements[1]
        arraws = sceneElements[2]
        self.scene.Id = sceneElements[3]
            
        for i in range(len(elements)):
                item = elements[i].getItem()
                item.setId(item.id)
                if item.getType() == 7:
                    string=item.toPlainText()
                    string=string.encode("UTF-8")
                    item.setHtml("<img src=\":/images/actor1.png\" />"+"<p align=\"center\">"+string+"</p>")
                self.scene.addItem(item)
                self.scene.elements.append(item)
        for i in range(len(pictures)):
                item = pictures[i].getItem()
                item.setId(item.id)
                self.scene.addItem(item)
                self.scene.pictures.append(item)
        for i in range(len(arraws)):
                item = arraws[i].getItem()
                e1 = self.scene.getElementsById(item.getIdStart())
                if e1 != None:
                    item.setStartItem(e1)
                e2 = self.scene.getElementsById(item.getIdEnd())
                if e2!=None and e1!=None:
                    item.setEndItem(e2)
                    e1.addArrow(item)
                    e2.addArrow(item)
                    self.scene.addItem(item)
                    self.scene.Arrows.append(item)
                    item.updatePosition()
            
    def deleteItem(self):
        isDeleted = False
        for item in self.scene.selectedItems():
            if isinstance(item, ElementDiagramm):
                item.removeArrows()
                self.scene.removeItem(item)
                self.scene.elements.remove(item)
                isDeleted = True
        for arrow in self.scene.selectedItems():
            if isinstance(arrow, TotalLineDiagram):
                arrow.removeArrows()
                if isinstance(arrow.startItem(),ElementDiagramm):
                    super(ElementDiagramm,arrow.startItem()).__thisclass__.removeArrow(arrow.startItem(),arrow)
                else:
                    super(TotalLineDiagram,arrow.startItem()).__thisclass__.removeArrow(arrow.startItem(),arrow)
                if isinstance(arrow.endItem(),ElementDiagramm):
                    super(ElementDiagramm,arrow.endItem()).__thisclass__.removeArrow(arrow.endItem(),arrow)
                else:
                    super(TotalLineDiagram,arrow.endItem()).__thisclass__.removeArrow(arrow.endItem(),arrow)
                self.scene.removeItem(arrow)
                self.scene.Arrows.remove(arrow)
                isDeleted = True
        for pic in self.scene.selectedItems():
            if isinstance(pic, PictureElement):
                self.scene.pictures.remove(pic)
                self.scene.removeItem(pic)
                isDeleted = True
        if(isDeleted == True):
            self.diagramChanged()
        self.scene.update()
            
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
    def textEndInserted(self):
        self.falseChecked()
        self.pointer.setChecked(True)
        #self.diagramChanged()
    def diagramChanged(self):
        self.scene.setChangeFlag(True)
        if self.currentFileName != "":
            self.setWindowTitle(unicode("UseCaseDiagram - " + self.currentFileName + " *","UTF-8"))
        else:
             self.setWindowTitle(unicode("UseCaseDiagram - Диаграмма *","UTF-8"))
        self.saveScenesElements()
        
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
        QtGui.QMessageBox.about(self, unicode("О программа UseCaseDiagram","UTF-8"),
                unicode("<p align=\"center\">ВОЛГОГРАДСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ</p> \
                <p align=\"center\">ФАКУЛЬТЕТ ЭЛЕКТРОНИКИ И ВЫЧИСЛИТЕЛЬНОЙ ТЕХНИКИ</p>\
                <p align=\"center\">КАФЕДРА ПРОГРАМНОГО ОБЕСПЕЧЕНИЯ АВТОМАТИЗИРОВАННЫХ СИСТЕМ</p>\
                <p>UseCaseDiagram - программа построения диагамм \"вариантов использования\"</p>\
                <p>Авторы:</p>\
                <p>Дмитриенко Д.В., Ли Е.В., Рашевский Н.М., Синицын А.А.</p>\
                <p><a href=\"http://code.google.com/p/usecasevstu/\" >http://code.google.com/p/usecasevstu/</a></p>\
                <p align=\"center\">Волгоград 2011</p>\
                ","UTF-8"))

    def createActions(self):

        self.arrowTotal = QtGui.QAction(
                QtGui.QIcon(':/images/linepointer.png'), unicode("Ассоциация","UTF-8"),
                self,shortcut="Ctrl+6",triggered = self.toArrowTotal
        )
        self.arrowTotal.setCheckable(True)
        self.arrowComment = QtGui.QAction(
                QtGui.QIcon(':/images/linedottedpointer.png'), unicode("Пунктирная линия","UTF-8"),
                self,shortcut="Ctrl+8",triggered = self.toArrowComment
        )
        self.arrowComment.setCheckable(True)
        self.arrow = QtGui.QAction(
                QtGui.QIcon(':/images/linepointerwhite.png'), unicode("Обобщение","UTF-8"),
                self,shortcut="Ctrl+7",triggered = self.toArrow
        )
        self.arrow.setCheckable(True)
        
        self.arrowInclude = QtGui.QAction(
                QtGui.QIcon(':/images/linepointerwhite.png'), unicode("Include","UTF-8"),
                self,shortcut="Ctrl+9",triggered = self.toArrowInclude
        )
        self.arrowInclude.setCheckable(True)
        
        self.arrowExtend = QtGui.QAction(
                QtGui.QIcon(':/images/linepointerwhite.png'), unicode("Extend","UTF-8"),
                self,shortcut="Ctrl+0",triggered = self.toArrowExtend
        )
        self.arrowExtend.setCheckable(True)
        
        self.arrowAgregation = QtGui.QAction(
                QtGui.QIcon(':/images/linepointerwhite.png'), unicode("Agregation","UTF-8"),
                self,shortcut="Ctrl+-",triggered = self.toArrowAgregation
        )
        self.arrowAgregation.setCheckable(True)

        
        self.useCaseAction = QtGui.QAction(
                QtGui.QIcon(':/images/usecase.png'), unicode("Вариант использования","UTF-8"),
                self,shortcut="Ctrl+2",triggered = self.toUseCase
        )
        self.useCaseAction.setCheckable(True)
        self.actorAction = QtGui.QAction(
                QtGui.QIcon(':/images/actor.png'), unicode("Участник","UTF-8"),
                self,shortcut="Ctrl+3",triggered = self.toActor
        )
        self.actorAction.setCheckable(True)
        self.commentAction = QtGui.QAction(
                QtGui.QIcon(':/images/comment.png'), unicode("Комментарий","UTF-8"),
                self,shortcut="Ctrl+4",triggered = self.toComment
        )
        self.commentAction.setCheckable(True)
        self.picAction = QtGui.QAction(
                QtGui.QIcon(':/images/pic.png'), unicode("Изображение","UTF-8"),
                self,shortcut="Ctrl+5",triggered = self.toPic
        )
        self.picAction.setCheckable(True)
        self.pointer = QtGui.QAction(
                QtGui.QIcon(':/images/pointer.png'), unicode("Выбрать","UTF-8"),
                self,shortcut="Ctrl+1",triggered = self.toPointer
        )
        self.pointer.setCheckable(True)
        self.createAction = QtGui.QAction( unicode("Создать","UTF-8"),
                self,shortcut="Ctrl+N",triggered = self.toCreateAction
        )
        self.openAction = QtGui.QAction( unicode("Открыть...","UTF-8"),
                self,shortcut="Ctrl+O",triggered = self.toOpenAction
        )
        self.saveAction = QtGui.QAction( unicode("Сохранить","UTF-8"),
                self,shortcut="Ctrl+S",triggered = self.toSaveAction
        )
        self.saveAsAction = QtGui.QAction( unicode("Сохранить как...","UTF-8"),
                self,shortcut="Ctrl+Shift+S",triggered = self.toSaveAsAction
        )
        self.saveToPicAction = QtGui.QAction( unicode("Сохранить в картинку...","UTF-8"),
                self,shortcut="Ctrl+I",triggered = self.toSaveToPicAction
        )
        #self.toFrontAction = QtGui.QAction(
        #        QtGui.QIcon(':/images/bringtofront.png'), "Bring to &Front",
        #        self, shortcut="Ctrl+F", statusTip="Bring item to front",
        #        triggered = self.bringToFront)

        #self.sendBackAction = QtGui.QAction(
        #        QtGui.QIcon(':/images/sendtoback.png'), "Send to &Back", self,
        #        shortcut="Ctrl+B", statusTip="Send item to back",
        #        triggered=self.sendToBack)

        self.sendBackAction = QtGui.QAction(
                QtGui.QIcon(':/images/sendtoback.png'), "Send to &Back", self,
                shortcut="Ctrl+B", statusTip="Send item to back",
                triggered=self.sendToBack)

        self.deleteAction = QtGui.QAction(QtGui.QIcon(':/images/delete.png'),
                unicode("Удалить","UTF-8"), self, shortcut="Backspace",triggered=self.deleteItem)
        
        self.undoAction = QtGui.QAction(QtGui.QIcon(':/images/undo.png'),
                            unicode("Отменить действие","UTF-8"), self, shortcut="Ctrl+Z",triggered=self.undo)
        self.undoAction.setEnabled(False)
        
        self.redoAction = QtGui.QAction(QtGui.QIcon(':/images/redo.png'),
                            unicode("Вернуть действие","UTF-8"), self, shortcut="Ctrl+Shift+Z",triggered=self.redo)
        self.redoAction.setEnabled(False)

        self.exitAction = QtGui.QAction(unicode("Выход","UTF-8"), self, shortcut="Ctrl+Q",
                statusTip="Quit Scenediagram example", triggered=self.close)
        self.aboutAction = QtGui.QAction(unicode("О программе","UTF-8"), self, shortcut="Ctrl+B",
                triggered=self.about)
        self.copyAction = QtGui.QAction(unicode("Копировать","UTF-8"), self, shortcut="Ctrl+C", triggered=self.toCopy)
        self.pasteAction = QtGui.QAction(unicode("Вставить","UTF-8"), self, shortcut="Ctrl+V", triggered=self.toPaste)
        self.cutAction = QtGui.QAction(unicode("Вырезать","UTF-8"), self, shortcut="Ctrl+X", triggered=self.toCut)
    def toCut(self):
        self.toCopy()
        self.deleteItem()
    def toCopy(self):
        copyStr = ""
        mostLeft = self.scene.widthWorkPlace
        mostTop = self.scene.heightWorkPlace
        mostLeftId = 0
        mostTopId = 0
        listLineNode=[]
        listLine=[]
        listNotLineElem = []
        listComLineNode = []
        #проверяем нет ли линий без вершин и определяем самый левый и верхний элемент из выделенных
        for item in self.scene.selectedItems():
            if isinstance(item,TotalLineDiagram):
                listLine.append(item.getId())
                listLineNode.append(item.startItem().getId())
                listLineNode.append(item.endItem().getId())
                if item.getType() == DiagramScene.CommentLineType:
                    listComLineNode.append(item.startItem().getId())
                    listComLineNode.append(item.endItem().getId())
            if isinstance(item,ElementDiagramm) or isinstance(item,PictureElement):
                listNotLineElem.append(item.getId())
                if mostLeft > item.x():
                    mostLeft = item.x()
                    mostLeftId = item.getId()
                if mostTop > item.y():
                    mostTop = item.y()
                    mostTopId = item.getId()
                    
        #listComLineNode = listComLineNode+listNotLineElem
        #listComLineNode = listComLineNode+listLineNode   
        allListLineNode = []
        allListLineNode = listLine + listNotLineElem
        for i in listLineNode:
            buf = i in allListLineNode
            if buf == False:
                #если есть стрелка без вершины, то вывод сообщения
                msgBox = QtGui.QMessageBox()
                msgBox.setText(unicode("Невозможно копировать выбранные элементы\nСтрелка должна быть привязана к двум элементам диаграммы","UTF-8"))
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                saveButton = msgBox.addButton(unicode("Ok","UTF-8"),QtGui.QMessageBox.YesRole)
                msgBox.exec_()
                return
        copyStr = copyStr + "D_U_C_P"  #код программы
        copyStr = copyStr + ":;:"      #разделители
        copyStr = copyStr + str(len(self.scene.selectedItems())) #кол-во выделенных элементов
        copyStr = copyStr + ":;:"
        copyStr = copyStr + str(len(listNotLineElem)) #кол-во выделенных элементов
        copyStr = copyStr + ":;:"
        # записываем элементы не линии
        for i in listNotLineElem:
            copyStr = copyStr + str(self.scene.getElementsById(i).getType())
            copyStr = copyStr + ":;:"
            copyStr = copyStr + str(i)
            copyStr = copyStr + ":;:"
            if isinstance(self.scene.getElementsById(i),PictureElement):
                copyStr = copyStr + "1"
                copyStr = copyStr + ":;:"
                copyStr = copyStr + self.scene.getElementsById(i).fileName
            else:
                copyStr = copyStr + "0"
                copyStr = copyStr + ":;:"
                copyStr = copyStr + self.scene.getElementsById(i).toPlainText()
            copyStr = copyStr + ":;:"
            copyStr = copyStr + str(self.scene.getElementsById(i).x() - mostLeft)
            copyStr = copyStr + ":;:"
            copyStr = copyStr + str(self.scene.getElementsById(i).y() - mostTop)
            copyStr = copyStr + ":;:"
        for i in listLine:
            copyStr = copyStr + str(self.scene.getElementsById(i).getType())
            copyStr = copyStr + ":;:"
            copyStr = copyStr + str(self.scene.getElementsById(i).startItem().getId())
            copyStr = copyStr + ":;:"
            copyStr = copyStr + str(self.scene.getElementsById(i).endItem().getId())
            copyStr = copyStr + ":;:"
            copyStr = copyStr + str(i)
            copyStr = copyStr + ":;:"
        myClipBoard = QtGui.QApplication.clipboard()
        myClipBoard.setText(copyStr)
    def toPaste(self):
        myClipBoard = QtGui.QApplication.clipboard()
        pasteStr=myClipBoard.text()
        pasteList = pasteStr.split(":;:")
        if pasteList[0]=="D_U_C_P":
            lastId = dict()
            i = 0
            while i < int(pasteList[2]):
                if int(pasteList[3+i*6]) == DiagramScene.ActorType:
                    item = Actor()
                elif int(pasteList[3+i*6]) == DiagramScene.CommentType:
                    item = Comment()
                elif int(pasteList[3+i*6]) == DiagramScene.UseCaseType:
                    item = UseCase()
                elif int(pasteList[3+i*6]) == DiagramScene.PictureType:
                    item = PictureElement(pasteList[6+i*6])
                item.setPos(QtCore.QPointF(float(pasteList[7+i*6]) + self.coordPaste.x(),float(pasteList[8+i*6])+self.coordPaste.y()))
                self.scene.Id = self.scene.Id + 1
                item.setId(self.scene.Id)
                lastId[int(pasteList[4+i*6])] = self.scene.Id
                if int(pasteList[3+i*6]) != DiagramScene.PictureType:
                    item.setPlainText(pasteList[6+i*6])
                    if item.getType() == 7:
                        string=item.toPlainText()
                        string=string.encode("UTF-8")
                        item.setHtml("<img src=\":/images/actor1.png\" />"+"<p align=\"center\">"+string+"</p>")
                    self.scene.elements.append(item)
                else:
                    self.scene.pictures.append(item)
                self.scene.addItem(item)
                i=i+1
            i = 0
            self.coordPaste = QtCore.QPointF(0,0)
            listComline = []
            lastIdLine = dict()
            while i < int(pasteList[1])-int(pasteList[2]):
                type = int(pasteList[3+int(pasteList[2])*6+ i*4])
                if type == DiagramScene.CommentLineType:
                    listComline.append(i)
                elif type == DiagramScene.ArrowAssociationType:
                    item = ArrowAssociation()
                elif type == DiagramScene.ArrowGeneralizationType:
                    item = ArrowGeneralization()
                elif type == DiagramScene.ArrowAgregationType:
                    item = ArrowAgregation()
                elif type == DiagramScene.ArrowExtendType:
                    item = ArrowExtend()
                elif type == DiagramScene.ArrowIncludeType:
                    item = ArrowInclude()
                if type != DiagramScene.CommentLineType:
                    item.setIdStart(lastId[int(pasteList[4+int(pasteList[2])*6 + i*4])])
                    item.setIdEnd(lastId[int(pasteList[5+int(pasteList[2])*6 + i*4])])
                    e1 = self.scene.getElementsById(item.getIdStart())
                    if e1 != None:
                        item.setStartItem(e1)
                    e2 = self.scene.getElementsById(item.getIdEnd())
                    if e2!=None and e1!=None:
                        item.setEndItem(e2)
                        e1.addArrow(item)
                        e2.addArrow(item)
                        self.scene.Id = self.scene.Id + 1
                        item.setId(self.scene.Id)
                        lastIdLine[int(pasteList[6+int(pasteList[2])*6 + i*4])] = self.scene.Id
                        self.scene.addItem(item)
                        self.scene.Arrows.append(item)
                        item.updatePosition()
                i=i+1
            for i in listComline:
                item = CommentLine()
                if lastIdLine.has_key(int(pasteList[4+int(pasteList[2])*6 + i*4])):
                    item.setIdStart(lastIdLine[int(pasteList[4+int(pasteList[2])*6 + i*4])])
                else:
                    item.setIdStart(lastId[int(pasteList[4+int(pasteList[2])*6 + i*4])])
                if lastIdLine.has_key(int(pasteList[5+int(pasteList[2])*6 + i*4])):
                    item.setIdEnd(lastIdLine[int(pasteList[5+int(pasteList[2])*6 + i*4])])
                else:
                    item.setIdStart(lastId[int(pasteList[4+int(pasteList[2])*6 + i*4])])
                e1 = self.scene.getElementsById(item.getIdStart())
                if e1 != None:
                    item.setStartItem(e1)
                e2 = self.scene.getElementsById(item.getIdEnd())
                if e2!=None and e1!=None:
                    item.setEndItem(e2)
                    e1.addArrow(item)
                    e2.addArrow(item)
                    self.scene.Id = self.scene.Id + 1
                    item.setId(self.scene.Id)
                    lastIdLine[int(6+int(pasteList[2])*6 + i*4)] = self.scene.Id
                    self.scene.addItem(item)
                    self.scene.Arrows.append(item)
                    item.updatePosition()
        self.scene.update()
    def clearAll(self):
        for item in self.scene.elements:
            item.removeArrows()
            item.arrows[:]=[]
            self.scene.elements.remove(item)
        self.scene.elements[:]=[]
        for item in self.scene.Arrows:
            item.removeArrows()
            item.arrows[:]=[]
            self.scene.Arrows.remove(item)
        self.scene.pictures[:] = []
        self.scene.Arrows[:]=[]
        self.scene.clear()
    def askSaveMessage(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(unicode("Файл был изменен.\nХотите сохранить изменения?","UTF-8"))
        msgBox.setIcon(QtGui.QMessageBox.Question)
        saveButton = QtGui.QPushButton()
        saveButton = msgBox.addButton(unicode("Сохранить","UTF-8"),QtGui.QMessageBox.YesRole)
        cancelButton = QtGui.QPushButton()
        cancelButton = msgBox.addButton(unicode("Не сохранять","UTF-8"),QtGui.QMessageBox.NoRole)
        msgBox.exec_()
        #msgBox..exec()
        if msgBox.clickedButton()==saveButton :
            return True
        else:
            return False
    def closeEvent(self,event):
        if self.scene.getChangeFlag()==True and self.askSaveMessage()==True:
            if self.currentFileName:
                self.toSave(self.currentFileName)
            else:
                self.toSaveAsAction()
        super(MainWindow, self).closeEvent(event)
        
    def toCreateAction(self):
        if self.scene.getChangeFlag()==True and self.askSaveMessage()==True :
            if self.currentFileName:
                self.toSave(self.currentFileName)
            else:
                self.toSaveAsAction()
        self.clearAll()
        self.scene.addRect(0.0,0.0, self.scene.widthWorkPlace, self.scene.heightWorkPlace,QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)),4.0),QtGui.QBrush(QtGui.QColor(255,255,255,255)))
        self.currentFileName=""
        self.setWindowTitle(unicode("UseCaseDiagram - Диаграмма","UTF-8"))
        self.scene.setChangeFlag(False)
        self.cleanScenesElements()
        self.saveScenesElements()
    def toOpenAction(self):
        if self.scene.getChangeFlag()==True and self.askSaveMessage()==True:
            self.toSaveAsAction()
        fileName,other=QtGui.QFileDialog.getOpenFileName(self,unicode("Открыть файл","UTF-8"),unicode(""),unicode("Use case by CommandBrain (*.vox)"))
        if fileName:
            self.clearAll()
            self.scene.addRect(0.0,0.0, self.scene.widthWorkPlace, self.scene.heightWorkPlace,QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)),4.0),QtGui.QBrush(QtGui.QColor(255,255,255,255)))
            #ifdef WIN32
            folders = unicode(fileName.replace("/","\\")).encode('UTF-8')
            #else
            folders = unicode(fileName).encode('UTF-8')
            #endif
            file = QtCore.QFile(folders)
            if file.open(QtCore.QIODevice.ReadWrite) == False:
                QtGui.QMessageBox.warning(self, 'Application', u('Cannot open file.'))
                return False
            _out = QtCore.QDataStream(file)
            count = _out.readInt32()
            for i in range(count):
                    elem = ElementData()
                    item = elem.read(_out)
                    item.setId(item.id)
                    if item.getType() == 7:
                        string=item.toPlainText()
                        string=string.encode("UTF-8")
                        item.setHtml("<img src=\":/images/actor1.png\" />"+"<p align=\"center\">"+string+"</p>")
                    self.scene.addItem(item)
                    self.scene.elements.append(item)
            count = _out.readInt32()
            for i in range(count):
                    elem = ElementData()
                    item = elem.read(_out)
                    item.setId(item.id)
                    self.scene.addItem(item)
                    self.scene.pictures.append(item)
            count = _out.readInt32()
            for i in range(count):
                    elem = ElementData()
                    item = elem.read(_out)
                    e1 = self.scene.getElementsById(item.getIdStart())
                    if e1 != None:
                        item.setStartItem(e1)
                    e2 = self.scene.getElementsById(item.getIdEnd())
                    if e2!=None and e1!=None:
                        item.setEndItem(e2)
                        e1.addArrow(item)
                        e2.addArrow(item)
                        self.scene.addItem(item)
                        self.scene.Arrows.append(item)
                        item.updatePosition()
            self.scene.Id = _out.readInt32()
            self.currentFileName=folders
            self.setWindowTitle(unicode("UseCaseDiagram - "+self.currentFileName,"UTF-8"))
            file.close()
            self.scene.setChangeFlag(False)
            self.cleanScenesElements()
            self.saveScenesElements()
    def toSaveAction(self):
        if self.scene.getChangeFlag()==True:
            if self.currentFileName:
                self.toSave(self.currentFileName)
            else:
                self.toSaveAsAction()
        self.scene.setChangeFlag(False)
        
    def toSave(self,path):
        #ifdef WIN32
        folders = unicode(path.replace("/","\\")).encode('UTF-8')
        #else
        folders = unicode(path).encode('UTF-8')
        #endif
        file = QtCore.QFile(folders)
        if file.open(QtCore.QIODevice.WriteOnly) == False:
            QtGui.QMessageBox.warning(self, 'Application', u'Cannot write file ')
            return False
        _out = QtCore.QDataStream(file)
        count = len(self.scene.getElements())
        _out.writeInt32(count)
        for i in self.scene.getElements():
            elem = ElementData(i)
            _out = elem.save(_out)
        count = len(self.scene.pictures)
        _out.writeInt32(count)
        for i in self.scene.pictures:
            elem = ElementData(i)
            _out = elem.save(_out)
        count = len(self.scene.Arrows)
        _out.writeUInt32(count)
        for i in self.scene.Arrows:
            elem = ElementData(i)
            _out = elem.save(_out)
        _out.writeInt32(self.scene.Id)
        self.currentFileName=folders
        self.setWindowTitle(unicode("UseCaseDiagram - "+self.currentFileName,"UTF-8"))
        file.close()
    def toSaveAsAction(self):
        fileName,other=QtGui.QFileDialog.getSaveFileName(self,unicode("Сохранение в файл","UTF-8"),unicode(""),unicode("Use case by CommandBrain (*.vox)"))
        if fileName:
            self.toSave(fileName)
        self.scene.setChangeFlag(False)
    def toSaveToPicAction(self):
       filename=QtGui.QFileDialog.getSaveFileName(self,unicode("Сохранение в картинку","UTF-8"),unicode(""),unicode("Images (*.png)"))
       img = QtGui.QImage(self.scene.width(),self.scene.height(), QtGui.QImage.Format_ARGB32_Premultiplied)
       p = QtGui.QPainter()
       p.begin(img)
       self.scene.render(p)
       p.end()
  
       img.save(unicode(filename[0]),"png")
       
    def toArrowTotal(self):
        self.scene.setMode(self.scene.InsertArrowAssociation)
        self.falseChecked()
        self.arrowTotal.setChecked(True)
        
    
    def toArrowComment(self):
        self.scene.setMode(self.scene.InsertCommentLine)
        self.falseChecked()
        self.arrowComment.setChecked(True)

    def toArrow(self):
        self.scene.setMode(self.scene.InsertArrowGeneralization)
        self.falseChecked()
        self.arrow.setChecked(True)
        
    def toArrowInclude(self):
        self.scene.setMode(self.scene.InsertArrowInclude)
        self.falseChecked()
        self.arrowInclude.setChecked(True)
    
    def toArrowExtend(self):
        self.scene.setMode(self.scene.InsertArrowExtend)
        self.falseChecked()
        self.arrowExtend.setChecked(True)
        
    def toArrowAgregation(self):
        self.scene.setMode(self.scene.InsertArrowAgregation)
        self.falseChecked()
        self.arrowAgregation.setChecked(True)    
        

    def toUseCase(self):
        self.scene.setMode(self.scene.InsertUseCase)
        self.falseChecked()
        self.useCaseAction.setChecked(True)

    def toActor(self):
        self.scene.setMode(self.scene.InsertActor)
        self.falseChecked()
        self.actorAction.setChecked(True)

    def toComment(self):
        self.scene.setMode(self.scene.InsertText)
        self.falseChecked()
        self.commentAction.setChecked(True)
        
    def toPic(self):
        fileName,other=QtGui.QFileDialog.getOpenFileName(self,unicode("Вставить картинку","UTF-8"),unicode(""),unicode("picture (*.png)"))
        if fileName:
            #ifdef WIN32
            folders = unicode(fileName.replace("/","\\")).encode('UTF-8')
            #else
            folders = unicode(fileName).encode('UTF-8')
            #endif
            self.scene.addPicture(folders)
        self.falseChecked()
        self.picAction.setCheckable(True)
        self.pointer.setChecked(True)
    def toPointer(self):
        self.scene.setMode(self.scene.MoveItem)
        self.falseChecked()
        self.pointer.setChecked(True)
    
    
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(unicode("Файл","UTF-8"))
        self.fileMenu.addAction(self.createAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.cutAction)
        self.fileMenu.addAction(self.copyAction)
        self.fileMenu.addAction(self.pasteAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.saveToPicAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        self.itemMenu = self.menuBar().addMenu(unicode("Редактирование","UTF-8"))
        self.itemMenu.addAction(self.undoAction)
        self.itemMenu.addAction(self.redoAction)
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(self.useCaseAction)
        self.itemMenu.addAction(self.actorAction)
        self.itemMenu.addAction(self.commentAction)
        self.itemMenu.addAction(self.picAction)
        self.itemMenu.addAction(self.arrowTotal)
        self.itemMenu.addAction(self.arrow)
        self.itemMenu.addAction(self.arrowComment)
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(self.deleteAction)
        #self.itemMenu.addAction(self.toFrontAction)
        #self.itemMenu.addAction(self.sendBackAction)

        self.aboutMenu = self.menuBar().addMenu(unicode("Помощь","UTF-8"))
        self.aboutMenu.addAction(self.aboutAction)
        
    def createToolbars(self):
        self.editToolBar = self.addToolBar(unicode("Редактирование","UTF-8"))
        #self.editToolBar.addAction(self.toFrontAction)
        #self.editToolBar.addAction(self.sendBackAction)
        self.editToolBar.addAction(self.pointer)
        self.editToolBar.addAction(self.useCaseAction)
        self.editToolBar.addAction(self.actorAction)
        self.editToolBar.addAction(self.commentAction)
        self.editToolBar.addAction(self.picAction)
        self.editToolBar.addAction(self.arrowTotal)
        self.editToolBar.addAction(self.arrow)
        self.editToolBar.addAction(self.arrowComment)
        self.editToolBar.addAction(self.arrowInclude)
        self.editToolBar.addAction(self.arrowExtend)
        self.editToolBar.addAction(self.arrowAgregation)
        
        self.editToolBar.addAction(self.deleteAction)
        
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.undoAction)
        self.editToolBar.addAction(self.redoAction)
 
        pointerButton = QtGui.QToolButton()
        pointerButton.setCheckable(True)
        pointerButton.setChecked(True)
        pointerButton.setIcon(QtGui.QIcon(':/images/pointer.png'))
        
        #linePointerButton = QtGui.QToolButton()
        #linePointerButton.setCheckable(True)
        #linePointerButton.setIcon(QtGui.QIcon(':/images/linepointer.png'))

        #self.pointerTypeGroup = QtGui.QButtonGroup()
        #self.pointerTypeGroup.addButton(pointerButton, DiagramScene.MoveItem)
        #self.pointerTypeGroup.addButton(linePointerButton,
        #        DiagramScene.InsertLine)
        #self.pointerTypeGroup.buttonClicked[int].connect(self.pointerGroupClicked)

        self.sceneScaleCombo = QtGui.QComboBox()
        self.sceneScaleCombo.addItems(["50%", "100%", "150%", "200%"])
        self.sceneScaleCombo.setCurrentIndex(1)
        self.sceneScaleCombo.currentIndexChanged[str].connect(self.sceneScaleChanged)

        self.pointerToolbar = self.addToolBar(unicode("Настройки","UTF-8"))
        #self.pointerToolbar.addWidget(pointerButton)
        #self.pointerToolbar.addWidget(linePointerButton)
        self.pointerToolbar.addWidget(self.sceneScaleCombo)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.show()

    sys.exit(app.exec_())
