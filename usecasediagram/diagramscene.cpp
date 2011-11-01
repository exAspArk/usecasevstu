#include <QtGui>

#include "diagramscene.h"
#include "arrow.h"

//! [0]
DiagramScene::DiagramScene(QMenu *itemMenu, QObject *parent)
    : QGraphicsScene(parent)
{
    myItemMenu = itemMenu;
    myMode = MoveItem;
    myItemType = DiagramItem::Step;
    line = 0;
    textItem = 0;
    myItemColor = Qt::white;
    myTextColor = Qt::black;
    myLineColor = Qt::black;  
    changed = false;
    imageItem = NULL;
}
//! [0]

QList<DiagramEllipseItem*> DiagramScene::getEllipseItemList() {
    return ellipseItemList;
}
QList<QGraphicsLineItem*> DiagramScene::getLineItemList() {
    return lineItemList;
}
QList<QGraphicsLineItem*> DiagramScene::getLineItem2List() {
    return lineItem2List;
}
QList<DiagramTextItem*> DiagramScene::getTextItemList() {
    return textItemList;
}
QList<DiagramActorItem*> DiagramScene::getActorItemList() {
    return actorItemList;
}
DiagramImageItem* DiagramScene::getImageItem() {
    return imageItem;
}

void DiagramScene::addEllipseItemList(DiagramEllipseItem* item) {
    ellipseItemList.append(item);
}
void DiagramScene::addLineItemList(QGraphicsLineItem* item) {
    lineItemList.append(item);
}
void DiagramScene::addLineItem2List(QGraphicsLineItem* item) {
    lineItem2List.append(item);
}
void DiagramScene::addTextItemList(DiagramTextItem* item) {
    textItemList.append(item);
}
void DiagramScene::addActorItemList(DiagramActorItem* item) {
    actorItemList.append(item);
}
void DiagramScene::setImageItem(DiagramImageItem* item) {
    imageItem = item;
}

//! [1]
void DiagramScene::setLineColor(const QColor &color)
{
    myLineColor = color;
    if (isItemChange(Arrow::Type)) {
        Arrow *item =
            qgraphicsitem_cast<Arrow *>(selectedItems().first());
        item->setColor(myLineColor);
        update();
    }
}
//! [1]

//! [2]
void DiagramScene::setTextColor(const QColor &color)
{
    myTextColor = color;
    if (isItemChange(DiagramTextItem::Type)) {
        DiagramTextItem *item =
            qgraphicsitem_cast<DiagramTextItem *>(selectedItems().first());
        item->setDefaultTextColor(myTextColor);
    }
}
//! [2]

//! [3]
void DiagramScene::setItemColor(const QColor &color)
{
    myItemColor = color;
    if (isItemChange(DiagramItem::Type)) {
        DiagramItem *item =
            qgraphicsitem_cast<DiagramItem *>(selectedItems().first());
        item->setBrush(myItemColor);
    }
}
//! [3]

//! [4]
void DiagramScene::setFont(const QFont &font)
{
    myFont = font;

    if (isItemChange(DiagramTextItem::Type)) {
        QGraphicsTextItem *item =
            qgraphicsitem_cast<DiagramTextItem *>(selectedItems().first());
        //At this point the selection can change so the first selected item might not be a DiagramTextItem
        if (item)
            item->setFont(myFont);
    }
}
//! [4]
void DiagramScene::setImage(QString filename)
{
    image=QImage(filename);
}
void DiagramScene::setMode(Mode mode)
{
    myMode = mode;
}

void DiagramScene::setItemType(DiagramItem::DiagramType type)
{
    myItemType = type;
}

//! [5]
void DiagramScene::editorLostFocus(DiagramTextItem *item)
{
    QTextCursor cursor = item->textCursor();
    cursor.clearSelection();
    item->setTextCursor(cursor);

    if (item->toPlainText().isEmpty()) {
        removeItem(item);
        item->deleteLater();
    }
}
//! [5]

//! [6]
void DiagramScene::imageOnScene()
{
    this->imageItem = new DiagramImageItem(this->image);
    addItem(imageItem);
	imageItem->setPos(0,0);
    this->update();
}
void DiagramScene::mousePressEvent(QGraphicsSceneMouseEvent *mouseEvent)
{
    if (mouseEvent->button() != Qt::LeftButton)
        return;

    DiagramItem *item;
    switch (myMode) {
        case InsertItem:
            /*item = new DiagramItem(myItemType, myItemMenu);
            item->setBrush(myItemColor);
            addItem(item);
            item->setPos(mouseEvent->scenePos());
            emit itemInserted(item);
            break;*/
			this->ellipseItem = new DiagramEllipseItem();
			ellipseItem->setFont(myFont);
			ellipseItem->setTextInteractionFlags(Qt::TextEditorInteraction);
			ellipseItem->setZValue(1000.0);
			/*connect(ellipseItem, SIGNAL(lostFocus(DiagramEllipseItem*)),
				this, SLOT(editorLostFocus(DiagramEllipseItem*)));
			connect(ellipseItem, SIGNAL(selectedChange(QGraphicsItem*)),
				this, SIGNAL(itemSelected(QGraphicsItem*)));*/
			addItem(ellipseItem);
			ellipseItem->setDefaultTextColor(myTextColor);
			ellipseItem->setPos(mouseEvent->scenePos());
            emit textInserted(textItem);
            ellipseItemList.append(ellipseItem);
			/*emit textInserted(ellipseItem);*/
            changed = true;
            break;
//! [6] //! [7]
        case InsertLine:
            line = new QGraphicsLineItem(QLineF(mouseEvent->scenePos(),
                                        mouseEvent->scenePos()));
            line->setPen(QPen(myLineColor, 2));
            myLine= AssociationLine;
            addItem(line);
            changed = true;
            break;
        case InsertLineGeneral:
            line = new QGraphicsLineItem(QLineF(mouseEvent->scenePos(),
                                        mouseEvent->scenePos()));
            line->setPen(QPen(myLineColor, 2));
            myLine= GeneralizationLine;
            addItem(line);
            changed = true;
            break;
        case InsertLineDotted:
            line = new QGraphicsLineItem(QLineF(mouseEvent->scenePos(),
                                        mouseEvent->scenePos()));
            line->setPen(QPen(myLineColor, 2));
            myLine= DottedLine;
            addItem(line);
            changed = true;
            break;
//! [7] //! [8]
        case InsertText:
            textItem = new DiagramTextItem();
            textItem->setFont(myFont);
            textItem->setTextInteractionFlags(Qt::TextEditorInteraction);
            textItem->setZValue(1000.0);
            connect(textItem, SIGNAL(lostFocus(DiagramTextItem*)),
                    this, SLOT(editorLostFocus(DiagramTextItem*)));
            connect(textItem, SIGNAL(selectedChange(QGraphicsItem*)),
                    this, SIGNAL(itemSelected(QGraphicsItem*)));
            addItem(textItem);
            textItem->setDefaultTextColor(myTextColor);
            textItem->setPos(mouseEvent->scenePos());
            emit textInserted(textItem);
            textItemList.append(textItem);
            changed = true;
            break;
            
        case InsertActor:
            actorItem = new DiagramActorItem();
            //actorItem->setFont(myFont);
            //actorItem->setTextInteractionFlags(Qt::TextEditorInteraction);
            actorItem->setZValue(1000.0);
            actorItem->setTextWidth(50);
            actorItem->setHtml(QString("<img src=\":/images/actor.png\" /><p>Actor</p>"));
            //actorItem->setTextInteractionFlags (Qt::NoTextInteraction);
            //textItem->setPlainText(QString("\n\n\n"));
            //connect(actorItem, SIGNAL(lostFocus(DiagramTextItem*)),
             //       this, SLOT(editorLostFocus(DiagramTextItem*)));
            //connect(actorItem, SIGNAL(selectedChange(QGraphicsItem*)),
            //        this, SIGNAL(itemSelected(QGraphicsItem*)));
            addItem(actorItem);
            //actorItem->setDefaultTextColor(myTextColor);
            actorItem->setPos(mouseEvent->scenePos());
            emit textInserted(textItem);
            actorItemList.append(actorItem);
            changed = true;
            break;

        
        
//! [8] //! [9]
    default:
        ;
    }
    QGraphicsScene::mousePressEvent(mouseEvent);
}
//! [9]

//! [10]
void DiagramScene::mouseMoveEvent(QGraphicsSceneMouseEvent *mouseEvent)
{
    if ((myMode == InsertLine || myMode == InsertLineGeneral || myMode == InsertLineDotted) && line != 0) {
        QLineF newLine(line->line().p1(), mouseEvent->scenePos());
        line->setLine(newLine);
    } else if (myMode == MoveItem) {
        QGraphicsScene::mouseMoveEvent(mouseEvent);
    }
    update();
}
//! [10]

//! [11]
void DiagramScene::mouseReleaseEvent(QGraphicsSceneMouseEvent *mouseEvent)
{
    if (line != 0 && (myMode == InsertLine || myMode == InsertLineGeneral || myMode == InsertLineDotted)) {
        QList<QGraphicsItem *> startItems = items(line->line().p1());
        if (startItems.count() && startItems.first() == line)
            startItems.removeFirst();
        QList<QGraphicsItem *> endItems = items(line->line().p2());
        if (endItems.count() && endItems.first() == line)
            endItems.removeFirst();

        removeItem(line);
        delete line;
//! [11] //! [12]

        if (startItems.count() > 0 && endItems.count() > 0 &&
            /*startItems.first()->type() == DiagramItem::Type &&
            endItems.first()->type() == DiagramItem::Type &&*/
            startItems.first() != endItems.first()) {
           //DiagramEllipseItem *startItem =
            //    qgraphicsitem_cast<DiagramEllipseItem *>(startItems.first());
            //DiagramEllipseItem *endItem =
             //   qgraphicsitem_cast<DiagramEllipseItem *>(endItems.first());
           QGraphicsTextItem *startItem = (QGraphicsTextItem*)startItems[0];
		   QGraphicsTextItem *endItem  = (QGraphicsTextItem*)endItems[0];
            Arrow *arrow = new Arrow(startItem, endItem, 0, 0, myLine);
            arrow->setColor(myLineColor);
            //startItem->addArrow(arrow);
           // endItem->addArrow(arrow);
            arrow->setZValue(-1000.0);
            addItem(arrow);
            arrow->updatePosition();
        }
    }
//! [12] //! [13]
    line = 0;
    QGraphicsScene::mouseReleaseEvent(mouseEvent);
    update();
}
//! [13]

//! [14]
bool DiagramScene::isItemChange(int type)
{
    foreach (QGraphicsItem *item, selectedItems()) {
        if (item->type() == type)
            return true;
    }
    return false;
}
//! [14]
