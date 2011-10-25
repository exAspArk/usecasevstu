#ifndef DIAGRAMSCENE_H
#define DIAGRAMSCENE_H

#include <QGraphicsScene>
#include "diagramitem.h"
#include "diagramtextitem.h"
#include "diagramellipseitem.h"
#include "diagramimageitem.h"
#include "diagramactoritem.h"
#include "declarationdatatypes.h"

QT_BEGIN_NAMESPACE
class QGraphicsSceneMouseEvent;
class QMenu;
class QPointF;
class QGraphicsLineItem;
class QFont;
class QGraphicsTextItem;
class QColor;
QT_END_NAMESPACE

//! [0]
class DiagramScene : public QGraphicsScene
{
    Q_OBJECT

public:
    enum Mode { InsertItem, InsertLine, InsertLineGeneral, InsertLineDotted, InsertText, MoveItem, InsertActor, InsertImage };
    
	DiagramScene(QMenu *itemMenu, QObject *parent = 0);
    QFont font() const
        { return myFont; }
    QColor textColor() const
        { return myTextColor; }
    QColor itemColor() const
        { return myItemColor; }
    QColor lineColor() const
        { return myLineColor; }
    void setLineColor(const QColor &color);
    void setTextColor(const QColor &color);
    void setItemColor(const QColor &color);
    void setFont(const QFont &font);
    void setImage(QString filename);
    void imageOnScene();
    
    QList<DiagramEllipseItem*> getEllipseItemList();
    QList<QGraphicsLineItem*> getLineItemList();
    QList<QGraphicsLineItem*> getLineItem2List();
    QList<DiagramTextItem*> getTextItemList();
    QList<DiagramActorItem*> getActorItemList();
    DiagramImageItem* getImageItem();
    
    void addEllipseItemList(DiagramEllipseItem*);
    void addLineItemList(QGraphicsLineItem*);
    void addLineItem2List(QGraphicsLineItem*);
    void addTextItemList(DiagramTextItem*);
    void addActorItemList(DiagramActorItem*);
    void setImageItem(DiagramImageItem*);

public slots:
    void setMode(Mode mode);
    void setItemType(DiagramItem::DiagramType type);
    void editorLostFocus(DiagramTextItem *item);

signals:
    void itemInserted(DiagramItem *item);
    void textInserted(QGraphicsTextItem *item);
    void itemSelected(QGraphicsItem *item);

protected:
    void mousePressEvent(QGraphicsSceneMouseEvent *mouseEvent);
    void mouseMoveEvent(QGraphicsSceneMouseEvent *mouseEvent);
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *mouseEvent);

private:
    bool isItemChange(int type);

    DiagramItem::DiagramType myItemType;
    QMenu *myItemMenu;
    Mode myMode;
    bool leftButtonDown;
    QPointF startPoint;
    QGraphicsLineItem *line;
    TypeLine myLine;
    QFont myFont;
    DiagramTextItem *textItem;
	DiagramEllipseItem *ellipseItem;
    QColor myTextColor;
    QColor myItemColor;
    QColor myLineColor;

    DiagramActorItem *actorItem;
    QImage image;
    
    QList<DiagramEllipseItem*> ellipseItemList;
    QList<QGraphicsLineItem*> lineItemList;
    QList<QGraphicsLineItem*> lineItem2List;
    QList<DiagramTextItem*> textItemList;
    QList<DiagramActorItem*> actorItemList;
    DiagramImageItem *imageItem;
    
};
//! [0]

#endif
