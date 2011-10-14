#ifndef DIAGRAMACTORIMAGEITEM_H
#define DIAGRAMACTORIMAGEITEM_H


#include <QGraphicsRectItem>
#include <QPainter>
#include <QStyleOptionGraphicsItem>
#include <QPainterPath>
#include "declarationdatatypes.h"

class DiagramActorImageItem: public QGraphicsRectItem
 {
    
 public:
     enum {Type = UserType + 6};
     DiagramActorImageItem(QGraphicsItem *parent = 0, QGraphicsScene *scene = 0);
     DiagramActorImageItem( QImage img );
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

#endif // DIAGRAMACTORIMAGEITEM_H
