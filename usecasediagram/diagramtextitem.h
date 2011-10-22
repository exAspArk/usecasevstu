#ifndef DIAGRAMTEXTITEM_H
#define DIAGRAMTEXTITEM_H

#include <QGraphicsTextItem>
#include <QLinearGradient>
#include <QPen>
#include <QPainter>
#include <QStyleOptionGraphicsItem>
#include "declarationdatatypes.h"

QT_BEGIN_NAMESPACE
class QPainter;
class QFocusEvent;
class QGraphicsItem;
class QGraphicsScene;
class QGraphicsSceneMouseEvent;
QT_END_NAMESPACE

//! [0]
class DiagramTextItem : public QGraphicsTextItem
{
    Q_OBJECT

public:
    enum { Type = UserType + 3 };

    DiagramTextItem(QGraphicsItem *parent = 0, QGraphicsScene *scene = 0);

    int type() const
        { return Type; }
	int typeElement() {return this->typeElementData;}

signals:
    void lostFocus(DiagramTextItem *item);
    void selectedChange(QGraphicsItem *item);

protected:
    QVariant itemChange(GraphicsItemChange change, const QVariant &value);

    void focusOutEvent(QFocusEvent *event);
    void mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event);
	void paint ( QPainter * painter, const QStyleOptionGraphicsItem * option, QWidget * widget )
	{
		QRectF rectf = option->exposedRect;
		// отрисовка по линиям пока думаем как сделать скошенный угол и нужен он вообще
		QPointF newPointTopRight = QPointF((rectf.topRight().x()- rectf.topLeft().x())*9.0/10.0,
			rectf.topLeft().y());
		QPointF newPointBottomRight  = QPointF(rectf.topRight().x(),
			(rectf.bottomRight().y() - rectf.topRight().y())*1.0/10.0);
		QLinearGradient linearGrad(newPointBottomRight, rectf.bottomLeft());
		linearGrad.setColorAt(0, Qt::white);
		linearGrad.setColorAt(1, QColor(255,130,80));
		painter->fillRect(rectf,QBrush(linearGrad));
		painter->drawLine(rectf.topLeft(),newPointTopRight);
		painter->drawLine(rectf.topLeft(),rectf.bottomLeft());
		painter->drawLine(rectf.bottomLeft(),rectf.bottomRight());
		// отрисовка половины линии 
		painter->drawLine(rectf.bottomRight(),newPointBottomRight);
		painter->drawLine(newPointTopRight,newPointBottomRight);
		QGraphicsTextItem::paint(painter,option,widget);
	}
private:
	enum TypeElement typeElementData;
};
//! [0]

#endif
