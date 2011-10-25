#ifndef DIAGRAMIMAGEITEM_H
#define DIAGRAMIMAGEITEM_H

#include <QGraphicsRectItem>
#include <QPainter>
#include <QStyleOptionGraphicsItem>
#include <QPainterPath>
#include "declarationdatatypes.h"

class DiagramImageItem: public QGraphicsRectItem
 {
 public:
      enum {Type = UserType + 7};
     DiagramImageItem(QGraphicsItem *parent = 0, QGraphicsScene *scene = 0);
     DiagramImageItem( QImage img );
     int type() const
	{ return Type; }
	int typeElement() {return this->typeElementData;}
     //int rtti () const { return imageRTTI; }
 protected:
     void paint( QPainter *, const QStyleOptionGraphicsItem *option, QWidget *widget );
 private:
     QImage image;
     QPixmap pixmap;

     enum TypeElement typeElementData;
 };
#endif //DIAGRAMIMAGEItem_H

