#include "diagramellipseitem.h"

DiagramEllipseItem::DiagramEllipseItem(QGraphicsItem *parent,QGraphicsScene *scene )
	: QGraphicsTextItem(parent,scene)
{
	setFlag(QGraphicsItem::ItemIsMovable);
	setFlag(QGraphicsItem::ItemIsSelectable);
	this->typeElementData = Ellipse;
}

DiagramEllipseItem::~DiagramEllipseItem()
{

}
QVariant DiagramEllipseItem::itemChange(GraphicsItemChange change,
									 const QVariant &value)
{
	if (change == QGraphicsItem::ItemSelectedHasChanged)
		emit selectedChange(this);
	return value;
}
//! [1]

//! [2]
void DiagramEllipseItem::focusOutEvent(QFocusEvent *event)
{
	setTextInteractionFlags(Qt::NoTextInteraction);
	emit lostFocus(this);
	QGraphicsTextItem::focusOutEvent(event);
}
//! [2]

//! [5]
void DiagramEllipseItem::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)
{
	if (textInteractionFlags() == Qt::NoTextInteraction)
		setTextInteractionFlags(Qt::TextEditorInteraction);
	QGraphicsTextItem::mouseDoubleClickEvent(event);
}
//! [5]

