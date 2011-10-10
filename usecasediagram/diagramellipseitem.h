#ifndef DIAGRAMELLIPSEITEM_H
#define DIAGRAMELLIPSEITEM_H

#include <QGraphicsTextItem>
#include "declarationdatatypes.h"

class DiagramEllipseItem : public QGraphicsTextItem
{
	Q_OBJECT
public:
	enum {Type = UserType + 5};
	DiagramEllipseItem(QGraphicsItem *parent, QGraphicsScene *scene = 0);
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
	
		QGraphicsTextItem::paint(painter,option,widget);
	}
private:
	enum TypeElement typeElementData;

	
};

#endif // DIAGRAMELLIPSEITEM_H
