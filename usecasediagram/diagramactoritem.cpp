#include "diagramactoritem.h"
#include "diagramscene.h"


DiagramActorItem::DiagramActorItem(QGraphicsItem *parent, QGraphicsScene *scene)
    : QGraphicsTextItem(parent, scene)
{
    setFlag(QGraphicsItem::ItemIsMovable);
    setFlag(QGraphicsItem::ItemIsSelectable);
	this->typeElementData = Comment;

}
QVariant DiagramActorItem::itemChange(GraphicsItemChange change,
                     const QVariant &value)
{
    if (change == QGraphicsItem::ItemSelectedHasChanged)
        emit selectedChange(this);
    return value;
}
void DiagramActorItem::focusOutEvent(QFocusEvent *event)
{
    QString str;
    setTextInteractionFlags(Qt::NoTextInteraction);
    str=this->toPlainText();
    int i=0;
    int pos=0;
    bool imgFlag=false;
    while(i<str.size()&&imgFlag!=true)
    {
        if(str.at(i).unicode()>256)
        {
            imgFlag=true;
            pos=i;
        }
        i++;
    }
    if(imgFlag==false)
    {
        this->setHtml(QString("<img src=\":/images/actor.png\" />")+"<p>"+str+"</p>");
    }
    if(imgFlag==true&&(pos-1)!=0)
    {
        this->setHtml(QString("<img src=\":/images/actor.png\" />")+"<p>"+str.right(str.size()-2-pos+1)+"</p>");
    }
    emit lostFocus(this);
    QGraphicsTextItem::focusOutEvent(event);
}
void DiagramActorItem::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)
{
    if (textInteractionFlags() == Qt::NoTextInteraction)
        setTextInteractionFlags(Qt::TextEditorInteraction);
    QGraphicsTextItem::mouseDoubleClickEvent(event);
}