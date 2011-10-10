#ifndef DIAGRAMTEXTITEM_H
#define DIAGRAMTEXTITEM_H

#include <QGraphicsTextItem>
#include <QLinearGradient>
#include <QPen>
#include <QPainter>
#include <QStyleOptionGraphicsItem>

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
		QPointF newPointTopRight = QPointF((rectf.topRight().x()- rectf.topLeft().x())*3.0/4.0,rectf.topLeft().y());
		painter->drawLine(rectf.topLeft(),rectf.topRight());
		painter->drawLine(rectf.topLeft(),rectf.bottomLeft());
		painter->drawLine(rectf.bottomLeft(),rectf.bottomRight());
		painter->drawLine(rectf.topRight(),rectf.bottomRight());
		//painter->drawEllipse(rectf);
		// градиент
		QLinearGradient linearGrad(rectf.topLeft(), rectf.bottomRight());
		linearGrad.setColorAt(0, Qt::white);
		linearGrad.setColorAt(1, QColor(255,130,80));
		painter->fillRect(rectf,QBrush(linearGrad));
		QGraphicsTextItem::paint(painter,option,widget);
	}
};
//! [0]

#endif
