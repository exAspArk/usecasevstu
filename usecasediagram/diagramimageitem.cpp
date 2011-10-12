#include "diagramimageitem.h"

DiagramImageItem::DiagramImageItem(QGraphicsItem *parent,QGraphicsScene *scene )
	: QGraphicsRectItem(parent,scene)
{
	setFlag(QGraphicsItem::ItemIsMovable);
	setFlag(QGraphicsItem::ItemIsSelectable);
	this->typeElementData = Image;
}

DiagramImageItem::DiagramImageItem(QImage img)
    : image(img)
{
    setRect(0, 0, image.width(), image.height());
    setFlag(ItemIsMovable);
    setFlag(QGraphicsItem::ItemIsSelectable);
 #if !defined(Q_WS_QWS)
     pixmap.convertFromImage(image, Qt::OrderedAlphaDither);
 #endif
}
void DiagramImageItem::paint( QPainter *p, const QStyleOptionGraphicsItem *option, QWidget * )
 {
 // On Qt/Embedded, we can paint a QImage as fast as a QPixmap,
 // but on other platforms, we need to use a QPixmap.
 #if defined(Q_WS_QWS)
     p->drawImage( option->exposedRect, image, option->exposedRect, Qt::OrderedAlphaDither );
 #else
     p->drawPixmap( option->exposedRect, pixmap, option->exposedRect );
 #endif
 }

