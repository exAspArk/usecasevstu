#ifndef DIAGRAMIMAGEITEM_H
#define DIAGRAMIMAGEITEM_H

#include <QGraphicsRectItem>
#include <QPainter>
#include <QStyleOptionGraphicsItem>

class DiagramImageItem: public QGraphicsRectItem
 {
 public:
     DiagramImageItem( QImage img );
     //int rtti () const { return imageRTTI; }
 protected:
     void paint( QPainter *, const QStyleOptionGraphicsItem *option, QWidget *widget );
 private:
     QImage image;
     QPixmap pixmap;
 };
#endif //DIAGRAMIMAGEItem_H

