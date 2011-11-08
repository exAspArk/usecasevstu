#
# coding: UTF-8
# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QString', 2)

# проверка комментария
import math


from PySide import QtCore, QtGui


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
            
def getPoints(calcType, startPoint, endPoint, width1, width2, height1, height2):

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
         self.arrowsComment = []
         self.id = -1
         self.type = DiagramScene.NonType

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
        pass
    
    def polygon(self):
        return QtGui.QPolygonF(self.boundingRect())

    def addArrow(self,item):
        self.arrowsComment.append(item)

    def removeArrow(self,arrow):
        try:
            self.arrowsComment.remove(arrow)
        except ValueError:
            pass
         
    def removeArrows(self):
        for arrow in self.arrowsComment[:]:
            arrow.startItem().removeArrow(arrow)
            arrow.endItem().removeArrow(arrow)
            self.scene().removeItem(arrow)
         
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
            return True
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
        arrowSize = 7.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        calcType = 4

        if type(myStartItem) == UseCase and type(myEndItem) == UseCase:
                calcType = 1
        if type(myStartItem) == UseCase and (type(myEndItem) == Comment or type(myEndItem) == Actor):
                calcType = 2
        if (type(myStartItem) == Comment or type(myStartItem) == Actor) and type(myEndItem) == UseCase:
                calcType = 3
        if (type(myStartItem) == Comment or type(myStartItem) == Actor) and (type(myEndItem) == Comment or type(myEndItem) == Actor):
                calcType = 4



        par1 = calcType
        par2 = self.mapFromItem(myStartItem, myStartItem.boundingRect().center())
        par3 = self.mapFromItem(myEndItem, myEndItem.boundingRect().center())
        par4 = myStartItem.boundingRect().width()
        par5 = myEndItem.boundingRect().width()
        par6 = myStartItem.boundingRect().height()
        par7 = myEndItem.boundingRect().height()
        points = getPoints(par1,par2,par3,par4,par5,par6,par7)

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
        arrowSize = 7.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        calcType = 4

        if type(myStartItem) == UseCase and type(myEndItem) == UseCase:
                calcType = 1
        if type(myStartItem) == UseCase and (type(myEndItem) == Comment or type(myEndItem) == Actor):
                calcType = 2
        if (type(myStartItem) == Comment or type(myStartItem) == Actor) and type(myEndItem) == UseCase:
                calcType = 3
        if (type(myStartItem) == Comment or type(myStartItem) == Actor) and (type(myEndItem) == Comment or type(myEndItem) == Actor):
                calcType = 4

        par1 = calcType
        par2 = self.mapFromItem(myStartItem, myStartItem.boundingRect().center())
        par3 = self.mapFromItem(myEndItem, myEndItem.boundingRect().center())
        par4 = myStartItem.boundingRect().width()
        par5 = myEndItem.boundingRect().width()
        par6 = myStartItem.boundingRect().height()
        par7 = myEndItem.boundingRect().height()
        points = getPoints(par1,par2,par3,par4,par5,par6,par7)

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

class ElementDiagramm(QtGui.QGraphicsTextItem):

    lostFocus = QtCore.Signal(QtGui.QGraphicsTextItem)

    selectedChange = QtCore.Signal(QtGui.QGraphicsItem)

    
    def __init__(self, parent=None, scene=None):
        super(ElementDiagramm, self).__init__(parent, scene)
        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.myTypeElement = DiagramScene.NonType
        self.arrows = []
        self.id = -1
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
            string=string.center(15)
            self.setPlainText(string)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.lostFocus.emit(self)
        
        super(ElementDiagramm, self).focusOutEvent(event)

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
        self.myTypeElement = DiagramScene.UseCaseType
        string=""
        string=string.center(20)
        self.setPlainText(string)
        
    def paint(self, painter, option, widget=None):
        bodyRect = self.boundingRect()
        painter.drawEllipse(bodyRect)
        listCoord = bodyRect.getCoords()
        x1 = listCoord[0]
        y1 = listCoord[1]
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
        self.myTypeElement = DiagramScene.ActorType
        self.setTextWidth(65);
        self.setHtml("<img src=\":/images/actor1.png\" /><p>Actor</p>");
        textcursor=self.textCursor()
        textcursor.movePosition(QtGui.QTextCursor.Down,QtGui.QTextCursor.MoveAnchor,1)
        textcursor.movePosition(QtGui.QTextCursor.EndOfLine,QtGui.QTextCursor.KeepAnchor,5)
        self.setTextCursor(textcursor)
         
    def paint(self, painter, option, widget=None):
        super(Actor, self).paint(painter, option, widget)
    def polygon(self):
        return QtGui.QPolygonF(self.boundingRect())
    def focusOutEvent(self, event):
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
            self.setHtml("<img src=\":/images/actor1.png\" />"+"<p>"+string+"</p>")
        #если картинка найдена
        if imgFlag==True and (pos-1)!=0:
            #если картинка без текста
            if len(string)-pos-4<=0:
                self.setHtml("<img src=\":/images/actor1.png\" /><p>Actor</p>");
            else:
                self.setHtml("<img src=\":/images/actor1.png\" />"+"<p>"+string[pos+4:]+"</p>")
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)        
        self.lostFocus.emit(self)

class DiagramScene(QtGui.QGraphicsScene):
   
    PictureType,ArrowGeneralizationType,CommentLineType, ArrowAssociationType,NonType,CommentType,UseCaseType,ActorType,InsertItem, InsertLine, InsertText, MoveItem,InsertCommentLine,InsertUseCase,InsertArrowAssociation,InsertArrowGeneralization,InsertActor,InsertPicture  = range(18)

    itemInserted = QtCore.Signal(ElementDiagramm)

    textInserted = QtCore.Signal(QtGui.QGraphicsTextItem)

    itemSelected = QtCore.Signal(QtGui.QGraphicsItem)
    textEndInserted = QtCore.Signal()

    elements = []
    Arrows = []
    pictures = []
    Id = 0
    changeFlag=False
    
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
        return None
    def checkPos (self,pos):
        currentPos=QtCore.QPointF()
        currentPos=pos
        flag=False
        if currentPos.y()>1000.0:
            flag=True
            currentPos.setY(980.0)
        if currentPos.y()<0.0:
            flag=True
            currentPos.setY(20.0)
        if currentPos.x()>1000.0:
            flag=True
            currentPos.setX(980.0)
        if currentPos.x()<0.0:
            flag=True
            currentPos.setX(20.0)
        return currentPos
        return flag
        #currentPos.
        
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
            #if self.myMode == self.InsertActor:
             #   textItem.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            self.addItem(textItem)
            textItem.setDefaultTextColor(self.myTextColor)
            textItem.setPos(self.checkPos(mouseEvent.scenePos()))
            self.changeFlag=True
            # увеличиваем идентификатор
            self.Id = self.Id + 1
            textItem.setId(self.Id)
            self.elements.append(textItem)
        super(DiagramScene, self).mousePressEvent(mouseEvent)
        self.update()
        
    def addPicture(self,fString):
        pic = PictureElement(fString)
        self.changeFlag=True
        #pic.selectedChange.connect(self.itemSelected)
        pic.setPos(QtCore.QPointF(0,0))
        self.Id = self.Id+1
        pic.setId(self.Id)
        self.pictures.append(pic)
        self.addItem(pic)
    def mouseMoveEvent(self, mouseEvent):
        if (self.myMode == self.InsertArrowAssociation or self.myMode == self.InsertArrowGeneralization or self.myMode == self.InsertCommentLine)  and self.line :
            newLine = QtCore.QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)
        elif self.myMode == self.MoveItem:           
            super(DiagramScene, self).mouseMoveEvent(mouseEvent)
        self.changeFlag=True
        self.update()

    def getElements(self):
        return self.elements
    
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
                     self.Id = self.Id + 1
                     arrow.setId(self.Id)
                     arrow.setColor(self.myLineColor)
                     arrow.setZValue(10.0)
                     self.addItem(arrow)
                     startItem.addArrow(arrow)
                     endItem.addArrow(arrow)
                     self.Arrows.append(arrow)
                     arrow.updatePosition()
        else:
            curitems=self.items()
            for item in curitems:
                item.setPos(self.checkPos(item.scenePos()))
                item.update()
                if isinstance(item,ElementDiagramm):
                    for arrow in item.arrows:
                        arrow.updatePosition()
        self.line = None
        #после добавления элемента, переходит в состояние перетаскивания
        self.myMode = self.MoveItem
        self.textEndInserted.emit()
        super(DiagramScene, self).mouseReleaseEvent(mouseEvent)
        self.update()

    def isItemChange(self, type):
        for item in self.selectedItems():
            if isinstance(item, type):
                self.changeFlag=True
                return True
        return False
    def getChangeFlag(self):
        return self.changeFlag
    def setChangeFlag(self,flag):
        self.changeFlag=flag

class MainWindow(QtGui.QMainWindow):
    InsertTextButton = 10
    currentFileName = ""

    def __init__(self):
        super(MainWindow, self).__init__()
                
        self.createActions()
        self.createMenus()
        self.scene = DiagramScene(self.itemMenu)
        self.scene.setSceneRect(QtCore.QRectF(0, 0, 1000, 1000))
        self.scene.addRect(0.0,0.0,1000.0,1000.0,QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)),4.0),QtGui.QBrush(QtGui.QColor(240,240,240,255)))
        self.scene.itemInserted.connect(self.itemInserted)
        self.scene.textInserted.connect(self.textInserted)
        self.scene.textEndInserted.connect(self.textEndInserted)
        self.scene.itemSelected.connect(self.itemSelected)
        self.createToolbars()

        layout = QtGui.QHBoxLayout()
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing,True)
        
        layout.addWidget(self.view)
        
        self.widget = QtGui.QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle(unicode("UseCaseDiagram - Диаграмма","UTF-8"))
        self.setWindowIcon(QtGui.QIcon(':/images/program.png'))
        self.pointer.setChecked(True)
        QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("UTF-8"));
        
        #self.scene.setMode(self.pointerTypeGroup.checkedId())
    def falseChecked(self):
        self.arrowTotal.setChecked(False)
        self.arrowComment.setChecked(False)
        self.arrow.setChecked(False)
        self.useCaseAction.setChecked(False)
        self.commentAction.setChecked(False)
        self.actorAction.setChecked(False)
        self.picAction.setChecked(False)
        self.pointer.setChecked(False)
    def deleteItem(self):
        for item in self.scene.selectedItems():
            if isinstance(item, ElementDiagramm):
                item.removeArrows()
                self.scene.removeItem(item)
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
        for pic in self.scene.selectedItems():
            if isinstance(pic, PictureElement):
                self.scene.pictures.remove(pic)
                self.scene.removeItem(pic)
    
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
                self,triggered = self.toArrowTotal
        )
        self.arrowTotal.setCheckable(True)
        self.arrowComment = QtGui.QAction(
                QtGui.QIcon(':/images/linedottedpointer.png'), unicode("Пунктирная линия","UTF-8"),
                self,triggered = self.toArrowComment
        )
        self.arrowComment.setCheckable(True)
        self.arrow = QtGui.QAction(
                QtGui.QIcon(':/images/linepointerwhite.png'), unicode("Обобщение","UTF-8"),
                self,triggered = self.toArrow
        )
        self.arrow.setCheckable(True)
        self.useCaseAction = QtGui.QAction(
                QtGui.QIcon(':/images/usecase.png'), unicode("Вариант использования","UTF-8"),
                self,triggered = self.toUseCase
        )
        self.useCaseAction.setCheckable(True)
        self.actorAction = QtGui.QAction(
                QtGui.QIcon(':/images/actor.png'), unicode("Участник","UTF-8"),
                self,triggered = self.toActor
        )
        self.actorAction.setCheckable(True)
        self.commentAction = QtGui.QAction(
                QtGui.QIcon(':/images/comment.png'), unicode("Комментарий","UTF-8"),
                self,triggered = self.toComment
        )
        self.commentAction.setCheckable(True)
        self.picAction = QtGui.QAction(
                QtGui.QIcon(':/images/pic.png'), unicode("Изображение","UTF-8"),
                self,triggered = self.toPic
        )
        self.picAction.setCheckable(True)
        self.pointer = QtGui.QAction(
                QtGui.QIcon(':/images/pointer.png'), unicode("Выбрать","UTF-8"),
                self,triggered = self.toPointer
        )
        self.pointer.setCheckable(True)
        self.createAction = QtGui.QAction( unicode("Создать","UTF-8"),
                self,triggered = self.toCreateAction
        )
        self.openAction = QtGui.QAction( unicode("Открыть...","UTF-8"),
                self,triggered = self.toOpenAction
        )
        self.saveAction = QtGui.QAction( unicode("Сохранить","UTF-8"),
                self,triggered = self.toSaveAction
        )
        self.saveAsAction = QtGui.QAction( unicode("Сохранить как...","UTF-8"),
                self,triggered = self.toSaveAsAction
        )
        self.saveToPicAction = QtGui.QAction( unicode("Сохранить в картинку...","UTF-8"),
                self,triggered = self.toSaveToPicAction
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
                unicode("Удаление","UTF-8"), self, shortcut="Delete",triggered=self.deleteItem)
        self.exitAction = QtGui.QAction(unicode("Выход","UTF-8"), self, shortcut="Ctrl+X",
                statusTip="Quit Scenediagram example", triggered=self.close)
        self.aboutAction = QtGui.QAction(unicode("О программе","UTF-8"), self, shortcut="Ctrl+B",
                triggered=self.about)
        
    def clearAll(self):
        for item in self.scene.elements:
            item.removeArrows()
            item.arrows[:]=[]
            self.scene.elements.remove(item)
        self.scene.elements[:]=[]
        for item in self.scene.Arrows:
            item.removeArrows()
            item.arrowsComment[:]=[]
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
        self.scene.addRect(0.0,0.0,1000.0,1000.0,QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)),4.0),QtGui.QBrush(QtGui.QColor(240,240,240,255)))
        self.currentFileName=""
        self.setWindowTitle(unicode("UseCaseDiagram - Диаграмма","UTF-8"))
        self.scene.setChangeFlag(False)
    def toOpenAction(self):
        if self.scene.getChangeFlag()==True and self.askSaveMessage()==True:
            self.toSaveAsAction()
        fileName,other=QtGui.QFileDialog.getOpenFileName(self,unicode("Открыть файл","UTF-8"),unicode(""),unicode("Use case by CommandBrain (*.vox)"))
        if fileName:
            self.clearAll()
            self.scene.addRect(0.0,0.0,1000.0,1000.0,QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0,255)),4.0),QtGui.QBrush(QtGui.QColor(240,240,240,255)))
            folders = unicode(fileName.replace("/","\\")).encode('UTF-8')
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
                    item.setHtml("<img src=\":/images/actor1.png\" />"+"<p>"+string+"</p>")
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
                item.setStartItem(e1)
                e2 = self.scene.getElementsById(item.getIdEnd())
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
            
    def toSaveAction(self):
        if self.scene.getChangeFlag()==True:
            if self.currentFileName:
                self.toSave(self.currentFileName)
            else:
                self.toSaveAsAction()
        self.scene.setChangeFlag(False)
    def toSave(self,path):
        folders = unicode(path.replace("/","\\")).encode('UTF-8')
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
            folders = unicode(fileName.replace("/","\\")).encode('UTF-8')
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
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.saveToPicAction)
        self.fileMenu.addAction(self.exitAction)

        self.itemMenu = self.menuBar().addMenu(unicode("Редактирование","UTF-8"))
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
        self.editToolBar.addAction(self.deleteAction)
        


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
