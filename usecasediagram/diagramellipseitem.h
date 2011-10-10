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

signals:
	void lostFocus(DiagramEllipseItem *item);
	void selectedChange(QGraphicsItem *item);

protected:
	QVariant itemChange(GraphicsItemChange change, const QVariant &value);

	void focusOutEvent(QFocusEvent *event);
	void mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event);
	void paint ( QPainter * painter, const QStyleOptionGraphicsItem * option, QWidget * widget )
	{
		QRadialGradient radialGrad(option->exposedRect.center(), option->exposedRect.height());
		radialGrad.setColorAt(1, Qt::yellow);
		radialGrad.setColorAt(0, Qt::white);
		QPainterPath _path;
		_path.addEllipse(option->exposedRect);
		painter->fillPath(_path,QBrush(radialGrad));
		painter->drawEllipse(option->exposedRect);
		QGraphicsTextItem::paint(painter,option,widget);
	}
private:
	enum TypeElement typeElementData;

	
};

#endif // DIAGRAMELLIPSEITEM_H
