#include <QtGui>

#include "arrow.h"


//const qreal Pi = 3.14;

Arrow::Arrow(QGraphicsTextItem *startItem, QGraphicsTextItem *endItem,
         QGraphicsItem *parent, QGraphicsScene *scene, TypeLine linetype)
    : QGraphicsLineItem(parent, scene)
{
    myStartItem = startItem;
    myEndItem = endItem;
	lineType = linetype;
    setFlag(QGraphicsItem::ItemIsSelectable, true);
    myColor = Qt::black;
    setPen(QPen(myColor, 2, Qt::SolidLine, Qt::RoundCap, Qt::RoundJoin));
}
//! [0]
//! [1]
QRectF Arrow::boundingRect() const
{
    qreal extra = (pen().width() + 20) / 2.0;

    return QRectF(line().p1(), QSizeF(line().p2().x() - line().p1().x(),
                                      line().p2().y() - line().p1().y()))
        .normalized()
        .adjusted(-extra, -extra, extra, extra);
}
//! [1]

//! [2]
QPainterPath Arrow::shape() const
{
    QPainterPath path = QGraphicsLineItem::shape();
    path.addPolygon(arrowHead);
    return path;
}
//! [2]

//! [3]
void Arrow::updatePosition()
{
    QLineF line(mapFromItem(myStartItem, 0, 0), mapFromItem(myEndItem, 0, 0));
    setLine(line);
}
//! [3]

QPair<QPointF, QPointF> getPoints(int calcType, QPointF startPoint, QPointF endPoint, float width1, float width2, float height1, float height2) 
{
	QPair<QPointF, QPointF> result;
	Arrow::LineCircleCalculation calc11 = Arrow::LineCircleCalculation(startPoint, endPoint, width1, height1);
	Arrow::LineCircleCalculation calc12 = Arrow::LineCircleCalculation(endPoint, startPoint, width2, height2);
	Arrow::LineCircleCalculation calc21 = Arrow::LineCircleCalculation(startPoint, endPoint, width1, height1);
	Arrow::LineRectCalculation calc22 = Arrow::LineRectCalculation(endPoint, startPoint, width2, height2);
	Arrow::LineRectCalculation calc31 = Arrow::LineRectCalculation(startPoint, endPoint, width1, height1);
	Arrow::LineCircleCalculation calc32 = Arrow::LineCircleCalculation(endPoint, startPoint, width2, height2);
	Arrow::LineRectCalculation calc41 = Arrow::LineRectCalculation(startPoint, endPoint, width1, height1);
	Arrow::LineRectCalculation calc42 = Arrow::LineRectCalculation(endPoint, startPoint, width2, height2)	;
	
	switch(calcType)
	{
		case 1://circle-circle
			result.first = calc11.getResult();
			result.second = calc12.getResult();			
		break;
		case 2://circle-rect
			result.first = calc21.getResult();
			result.second = calc22.getResult();
		break;
		case 3://rect-circle
			result.first = calc31.getResult();
			result.second = calc32.getResult();
		break;
		case 4://rect-rect
			result.first = calc41.getResult();
			result.second = calc42.getResult();
		break;
	}
	
	
	return result;
}
//! [4]
void Arrow::paint(QPainter *painter, const QStyleOptionGraphicsItem *,
          QWidget *)
{
    if (myStartItem->collidesWithItem(myEndItem))
        return;

    QPen myPen = pen();
    myPen.setColor(myColor);
    qreal arrowSize = 7;
    painter->setPen(myPen);
    painter->setBrush(myColor);
//! [4] //! [5]
	int calcType = 1;
		
	if(myStartItem->type() == DiagramEllipseItem::Type && myEndItem->type() == DiagramEllipseItem::Type)
			calcType = 1;
	if(myStartItem->type() == DiagramEllipseItem::Type && 
		(myEndItem->type() == DiagramTextItem::Type || 
		myEndItem->type() == DiagramActorItem::Type || 
		myEndItem->type() == DiagramImageItem::Type))
			calcType = 2;
	if((myStartItem->type() == DiagramTextItem::Type || 
		myStartItem->type() == DiagramActorItem::Type || 
		myStartItem->type() == DiagramImageItem::Type) && myEndItem->type() == DiagramEllipseItem::Type)
			calcType = 3;
	if(
		(myStartItem->type() == DiagramTextItem::Type || 
		myStartItem->type() == DiagramActorItem::Type || 
		myStartItem->type() == DiagramImageItem::Type)
		&&
		(myEndItem->type() == DiagramTextItem::Type || 
		myEndItem->type() == DiagramActorItem::Type || 
		myEndItem->type() == DiagramImageItem::Type)
		)
			calcType = 4;




	//-----------
	int par1 = calcType;
	QPointF par2 = mapFromItem(myStartItem, myStartItem->boundingRect().center());
	QPointF par3 = mapFromItem(myEndItem, myEndItem->boundingRect().center());
	float par4 = myStartItem->boundingRect().width();
	float par5 = myEndItem->boundingRect().width();
	float par6 = myStartItem->boundingRect().height();
	float par7 = myEndItem->boundingRect().height();
	QPair<QPointF, QPointF> points = getPoints(par1,par2,par3,par4,par5,par6,par7);
    //QLineF centerLine(myStartItem->pos(), myEndItem->pos());
	QLineF centerLine(points.second, points.first);
	
	



    /*QPolygonF endPolygon = myEndItem->polygon();
    QPointF p1 = endPolygon.first() + myEndItem->pos();
    QPointF p2;
    QPointF intersectPoint;
    QLineF polyLine;
    for (int i = 1; i < endPolygon.count(); ++i) {
    p2 = endPolygon.at(i) + myEndItem->pos();
    polyLine = QLineF(p1, p2);
    QLineF::IntersectType intersectType =
        polyLine.intersect(centerLine, &intersectPoint);
    if (intersectType == QLineF::BoundedIntersection)
        break;
        p1 = p2;
    }*/

    //setLine(QLineF(intersectPoint, myStartItem->pos()));
	setLine(centerLine);
//! [5] //! [6]

    double angle = ::acos(line().dx() / line().length());
	if(line().dy() >= 0)
		angle = 2*Pi - angle;
    QPointF arrowP1;
	QPointF arrowP2;
	
    
//! [6] //! [7]
	switch(lineType){
		case AssociationLine:
			arrowP1 = line().p1() + QPointF(sin(angle + Pi / 3) * arrowSize,
                                        cos(angle + Pi / 3) * arrowSize);
			arrowP2 = line().p1() + QPointF(sin(angle + Pi - Pi / 3) * arrowSize,
                                        cos(angle + Pi - Pi / 3) * arrowSize);
			painter->drawLine(line());
			painter->drawLine(QLineF(line().p1(), arrowP1));
			painter->drawLine(QLineF(line().p1(), arrowP2));
		break;
		case DottedLine:
			painter->setPen(QPen(myColor, 1, Qt::DashLine));
			painter->drawLine(line());
		break;
		case GeneralizationLine:
			arrowSize = 9;
			arrowP1 = line().p1() + QPointF(sin(angle + Pi / 3) * arrowSize,
                                        cos(angle + Pi / 3) * arrowSize);
			arrowP2 = line().p1() + QPointF(sin(angle + Pi - Pi / 3) * arrowSize,
                                        cos(angle + Pi - Pi / 3) * arrowSize);
			arrowHead.clear();
			arrowHead << arrowP1 << line().p1() <<  arrowP2;
			painter->setBrush(Qt::white);
			painter->drawLine(line());
			painter->drawPolygon(arrowHead);
		break;	
	}
	//painter->drawPolygon(arrowHead);
    if (isSelected()) {
        painter->setPen(QPen(myColor, 1, Qt::DashLine));
		QLineF myLine = line();
		myLine.translate(0, 4.0);
		painter->drawLine(myLine);
		myLine.translate(0,-8.0);
		painter->drawLine(myLine);
	}
	this->scene()->update();
}
//! [7]
