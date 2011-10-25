#ifndef DIAGRAMACTORITEM_H
#define DIAGRAMACTORITEM_H

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


class DiagramActorItem : public QGraphicsTextItem
{
     Q_OBJECT

public:
    enum { Type = UserType + 10 };

    DiagramActorItem(QGraphicsItem *parent = 0, QGraphicsScene *scene = 0);

    int type() const
        { return Type; }
	int typeElement() {return this->typeElementData;}

	friend QDataStream &operator << (QDataStream &stream, DiagramActorItem *actorItem) {
        stream << actorItem->toHtml();
        stream << actorItem->pos();
        return stream;
    }
    friend QDataStream &operator >> (QDataStream &stream, DiagramActorItem *actorItem) {
        QString text;
        QPointF pos;
        
        stream >> text;
        stream >> pos;

        actorItem->setHtml(text);
        actorItem->setPos(pos);
        return stream;
    }

signals:
    void lostFocus(DiagramActorItem *item);
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

#endif // DIAGRAMACTORITEM_H
