#ifndef DIAGRAMELLIPSEITEM_H
#define DIAGRAMELLIPSEITEM_H

#include <QGraphicsTextItem>
#include <QPainter>
#include <QStyleOptionGraphicsItem>
#include <QPainterPath>
#include "declarationdatatypes.h"

class DiagramEllipseItem : public QGraphicsTextItem
{
	Q_OBJECT
public:
	enum {Type = UserType + 5};
	DiagramEllipseItem(QGraphicsItem *parent = 0, QGraphicsScene *scene = 0);
	~DiagramEllipseItem();
	int type() const
	{ return Type; }
	int typeElement() {return this->typeElementData;}
	QPolygonF polygon() const
	{
		QPainterPath _path;
		_path.addEllipse(this->rectF);
		return _path.toFillPolygon();
	}
signals:
	void lostFocus(DiagramEllipseItem *item);
	void selectedChange(QGraphicsItem *item);

protected:
	QVariant itemChange(GraphicsItemChange change, const QVariant &value);

	void focusOutEvent(QFocusEvent *event);
	void mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event);
	void paint ( QPainter * painter, const QStyleOptionGraphicsItem * option, QWidget * widget )
	{
		this->rectF = option->exposedRect;
		qreal x1=0;
		qreal y1=0;
		qreal x2=0;
		qreal y2=0;
		option->exposedRect.getCoords(&x1,&y1,&x2,&y2);
		QRadialGradient radialGrad(QPointF(x1,y1), option->exposedRect.height());
		radialGrad.setColorAt(1, QColor(255,160,25));
		radialGrad.setColorAt(0.5,Qt::yellow);
		radialGrad.setColorAt(0, Qt::white);
		QPainterPath _path;
		_path.addEllipse(option->exposedRect);
		painter->fillPath(_path,QBrush(radialGrad));
		painter->drawEllipse(option->exposedRect);
		QGraphicsTextItem::paint(painter,option,widget);
	}
private:
	enum TypeElement typeElementData;
	QRectF rectF;
};

#endif // DIAGRAMELLIPSEITEM_H
