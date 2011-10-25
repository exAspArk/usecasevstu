#ifndef ARROW_H
#define ARROW_H

#include <QGraphicsLineItem>
#include "math.h"
#include "diagramitem.h"
#include "diagramellipseitem.h"
#include "declarationdatatypes.h"
#include "diagramtextitem.h"
#include "diagramellipseitem.h"
#include "diagramimageitem.h"
#include "diagramactoritem.h"

#include <QPair>
QT_BEGIN_NAMESPACE
class QGraphicsPolygonItem;
class QGraphicsLineItem;
class QGraphicsScene;
class QRectF;
class QGraphicsSceneMouseEvent;
class QPainterPath;
QT_END_NAMESPACE

//! [0]
class Arrow : public QGraphicsLineItem
{
public:
    enum { Type = UserType + 4 };
	enum DiagramType { Step, Conditional, StartEnd, Io };
	//enum TypeLine {AssociationLine, GeneralizationLine, DottedLine};
	class LineCircleCalculation 
	{
	public:
		float x1,x2_1,x2_2,x3;
		float y1,y2_1,y2_2,y3;
		float w,h;
		float line_k, line_b;
		LineCircleCalculation(QPointF circleCenter, QPointF outerPoint, float circleWidth, float circleHeight)
		{
			x1 = circleCenter.x();
			y1 = circleCenter.y();
			x3 = outerPoint.x();
			y3 = outerPoint.y();
			w = circleWidth;
			h = circleHeight;
			line_k = (y3-y1)/(x3-x1);
			line_b = y1 - x1*(y3-y1)/(x3-x1);
		}
		bool checkPoint(float x, float y)
		{
			bool result = false;
			result = sqrt((x3-x)*(x3-x) + (y3-y)*(y3-y)) < sqrt((x3-x1)*(x3-x1) + (y3-y1)*(y3-y1));
			return result;
		}
		QPointF getResult() 
		{
			float res_x = 0;
			float res_y = 0;
			
			
			float angle = atanf(line_k);
			x2_1 = x1 + w*cosf(angle)/2;
			y2_1 = y1 + h*sinf(angle)/2;

			x2_2 = x1 - w*cosf(angle)/2;
			y2_2 = y1 - h*sinf(angle)/2;
			
			
			if(checkPoint(x2_1, y2_1))
			{
				res_x = x2_1;
				res_y = y2_1;
			}
			else 
			{
				if(checkPoint(x2_2, y2_2))
				{
					res_x = x2_2;
					res_y = y2_2;
				}
			}
			
			QPointF res(res_x, res_y);
			return res;
		}
	};
	class LineRectCalculation 
	{
	public:
		float x1,x2_1,x2_2,x3;
		float y1,y2_1,y2_2,y3;
		float w,h;
		float line_k, line_b;
		LineRectCalculation(QPointF rectCenter, QPointF outerPoint, float rectWidth, float rectHeight)
		{
			x1 = rectCenter.x();
			y1 = rectCenter.y();
			x3 = outerPoint.x();
			y3 = outerPoint.y();
			w = rectWidth;
			h = rectHeight;
			line_k = (y3-y1)/(x3-x1);
			line_b = y1 - x1*(y3-y1)/(x3-x1);
		}
		bool checkPoint(float x, float y)
		{
			bool result = false;
			result = sqrt((x3-x)*(x3-x) + (y3-y)*(y3-y)) < sqrt((x3-x1)*(x3-x1) + (y3-y1)*(y3-y1));
			return result;
		}
		QPointF getResult() 
		{
			float res_x = 0;
			float res_y = 0;
			
			
			float angle = atanf(line_k);
			
			if(angle < atanf(h/w))
			{
				x2_1 = x1 + w/2;
				y2_1 = y1 + h*sinf(angle)/2;

				x2_2 = x1 - w/2;
				y2_2 = y1 - h*sinf(angle)/2;
			}
			else
			{
				y2_1 = y1 + h/2;
				x2_1 = x1 + w*cosf(angle)/2;

				y2_2 = y1 - h/2;
				x2_2 = x1 - w*cosf(angle)/2;
			}
			
			if(checkPoint(x2_1, y2_1))
			{
				res_x = x2_1;
				res_y = y2_1;
			}
			else 
			{
				if(checkPoint(x2_2, y2_2))
				{
					res_x = x2_2;
					res_y = y2_2;
				}
			}
			
			QPointF res(res_x, res_y);
			return res;
		}
	};


    Arrow(QGraphicsTextItem *startItem, QGraphicsTextItem *endItem,
      QGraphicsItem *parent = 0, QGraphicsScene *scene = 0, TypeLine linetype = AssociationLine);
void setLineType(TypeLine newLineType); 
    int type() const
        { return Type; }
    QRectF boundingRect() const;
    QPainterPath shape() const;
    void setColor(const QColor &color)
        { myColor = color; }
    QGraphicsTextItem *startItem() const
        { return myStartItem; }
    QGraphicsTextItem *endItem() const
        { return myEndItem; }
	DiagramEllipseItem* ellipseItem(QGraphicsTextItem* item){return qgraphicsitem_cast<DiagramEllipseItem*>(item);}

public slots:
    void updatePosition();

protected:
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option,
               QWidget *widget = 0);


private:
    QGraphicsTextItem *myStartItem;
    QGraphicsTextItem *myEndItem;
    QColor myColor;
    QPolygonF arrowHead;
	TypeLine lineType;
	
};
//! [0]

#endif
