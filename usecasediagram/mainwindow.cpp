#include <QtGui>

#include <QLabel>



#include "mainwindow.h"

#include "diagramitem.h"

#include "diagramscene.h"

#include "diagramtextitem.h"

#include "arrow.h"



const int InsertTextButton = 10;



//! [0]

MainWindow::MainWindow()

{

	 QTextCodec *codec = QTextCodec::codecForName("UTF8");

     QTextCodec::setCodecForTr(codec);

    // создаём экшены

    createActions();



    // createToolBox();



    // создадим менюшки

    createMenus();

	//сцена

    scene = new DiagramScene(itemMenu, this);

	scene->setSceneRect(QRectF(0, 0, 1280, 1024));

	// сигнал при нажатии на сцену передаёт объект который доюавляем

    connect(scene, SIGNAL(itemInserted(DiagramItem*)),

            this, SLOT(itemInserted(DiagramItem*)));

	// сигнал при добавлении на сцену текстовой надписи

    connect(scene, SIGNAL(textInserted(QGraphicsTextItem*)),

        this, SLOT(textInserted(QGraphicsTextItem*)));

	// когда выделяется элемент на сцене

    connect(scene, SIGNAL(itemSelected(QGraphicsItem*)),

        this, SLOT(itemSelected(QGraphicsItem*)));

	// созадаём тулбар

    createToolbars();

    QHBoxLayout *layout = new QHBoxLayout;

    //layout->addWidget(toolBox);

    view = new QGraphicsView(scene);

    layout->addWidget(view);



    QWidget *widget = new QWidget;

    widget->setLayout(layout);



    setCentralWidget(widget);

    setWindowTitle(tr("UseCase Diagram"));

    setUnifiedTitleAndToolBarOnMac(true);

    sceneScaleChanged(QString("100%"));

    this->view->setRenderHint(QPainter::Antialiasing,true);

}

//! [0]



//! [2]

void MainWindow::buttonGroupClicked(int id)

{

    QList<QAbstractButton *> buttons = buttonGroup->buttons();

    foreach (QAbstractButton *button, buttons) {

    if (buttonGroup->button(id) != button)

        button->setChecked(false);

    }

    if (id == InsertTextButton) {

        scene->setMode(DiagramScene::InsertText);

    } else {

        scene->setItemType(DiagramItem::DiagramType(id));

        scene->setMode(DiagramScene::InsertItem);

    }

}

//! [2]



//! [3]

void MainWindow::deleteItem()

{

    foreach (QGraphicsItem *item, scene->selectedItems()) {

        if (item->type() == Arrow::Type) {

            scene->removeItem(item);

           /* Arrow *arrow = qgraphicsitem_cast<Arrow *>(item);

            arrow->startItem()->removeArrow(arrow);

            arrow->endItem()->removeArrow(arrow);*/

            delete item;

        }

    }



    foreach (QGraphicsItem *item, scene->selectedItems()) {

         if (item->type() == DiagramItem::Type) {

             qgraphicsitem_cast<DiagramItem *>(item)->removeArrows();

         }

         scene->removeItem(item);

         delete item;

     }

}

//! [3]



//! [4]

void MainWindow::pointerGroupClicked(int)

{

    scene->setMode(DiagramScene::Mode(pointerTypeGroup->checkedId()));

}

//! [4]



//! [5]

void MainWindow::bringToFront()

{

    if (scene->selectedItems().isEmpty())

        return;



    QGraphicsItem *selectedItem = scene->selectedItems().first();

    QList<QGraphicsItem *> overlapItems = selectedItem->collidingItems();



    qreal zValue = 0;

    foreach (QGraphicsItem *item, overlapItems) {

        if (item->zValue() >= zValue &&

            item->type() == DiagramItem::Type)

            zValue = item->zValue() + 0.1;

    }

    selectedItem->setZValue(zValue);

}

//! [5]



//! [6]

void MainWindow::sendToBack()

{

    if (scene->selectedItems().isEmpty())

        return;



    QGraphicsItem *selectedItem = scene->selectedItems().first();

    QList<QGraphicsItem *> overlapItems = selectedItem->collidingItems();



    qreal zValue = 0;

    foreach (QGraphicsItem *item, overlapItems) {

        if (item->zValue() <= zValue &&

            item->type() == DiagramItem::Type)

            zValue = item->zValue() - 0.1;

    }

    selectedItem->setZValue(zValue);

}

//! [6]



//! [7]

void MainWindow::itemInserted(DiagramItem *item)

{

    pointerTypeGroup->button(int(DiagramScene::MoveItem))->setChecked(true);

    scene->setMode(DiagramScene::Mode(pointerTypeGroup->checkedId()));

    //buttonGroup->button(int(item->diagramType()))->setChecked(false);

}

//! [7]



//! [8]

void MainWindow::textInserted(QGraphicsTextItem *)

{

    //buttonGroup->button(InsertTextButton)->setChecked(false);

    scene->setMode(DiagramScene::Mode(pointerTypeGroup->checkedId()));

}

//! [8]



//! [9]

void MainWindow::currentFontChanged(const QFont &)

{

    handleFontChange();

}

//! [9]



//! [10]

void MainWindow::fontSizeChanged(const QString &)

{

    handleFontChange();

}

//! [10]



//! [11]

void MainWindow::sceneScaleChanged(const QString &scale)

{

    double newScale = scale.left(scale.indexOf(tr("%"))).toDouble() / 100.0;

    QMatrix oldMatrix = view->matrix();

    view->resetMatrix();

    view->translate(oldMatrix.dx(), oldMatrix.dy());

    view->scale(newScale, newScale);

}

//! [11]



//! [15]

void MainWindow::textButtonTriggered()

{

    scene->setTextColor(qVariantValue<QColor>(textAction->data()));

}

//! [15]



//! [16]

void MainWindow::fillButtonTriggered()

{

    scene->setItemColor(qVariantValue<QColor>(fillAction->data()));

}

//! [16]



//! [17]

void MainWindow::lineButtonTriggered()

{

    scene->setLineColor(qVariantValue<QColor>(lineAction->data()));

}

//! [17]



//! [18]

void MainWindow::handleFontChange()

{

    QFont font = fontCombo->currentFont();

    font.setPointSize(fontSizeCombo->currentText().toInt());

    font.setWeight(boldAction->isChecked() ? QFont::Bold : QFont::Normal);

    font.setItalic(italicAction->isChecked());

    font.setUnderline(underlineAction->isChecked());



    scene->setFont(font);

}

//! [18]



//! [19]

void MainWindow::itemSelected(QGraphicsItem *item)

{

    DiagramTextItem *textItem =

    qgraphicsitem_cast<DiagramTextItem *>(item);



    QFont font = textItem->font();

    QColor color = textItem->defaultTextColor();

    //fontCombo->setCurrentFont(font);

    //fontSizeCombo->setEditText(QString().setNum(font.pointSize()));

    //boldAction->setChecked(font.weight() == QFont::Bold);

    //italicAction->setChecked(font.italic());

    //underlineAction->setChecked(font.underline());

}

//! [19]



//! [20]

void MainWindow::about()

{

    QMessageBox::about(this, tr("usecase диаграмма"),

        tr("Выполнили студенты группы ИВТ-460:"

        "<p>Дмитриенко Д.В.</p>"

        "<p>Рашевский Н.М.</p>"

        "<p>Синицын А.А.</p>"));

}

//! [20]



//! [21]

void MainWindow::createToolBox()

{

}

//! [22]



//! [23]

void MainWindow::createActions()

{

    deleteAction = new QAction(QIcon(":/images/delete.png"),

                               tr("&Удалить"), this);

    deleteAction->setShortcut(tr("Удалить"));

    deleteAction->setStatusTip(tr("Удалить элемент с диаграммы"));

    connect(deleteAction, SIGNAL(triggered()),

        this, SLOT(deleteItem()));



    exitAction = new QAction(tr("Выход"), this);

    exitAction->setShortcuts(QKeySequence::Quit);

    exitAction->setStatusTip(tr("Выход из редактора"));

    connect(exitAction, SIGNAL(triggered()), this, SLOT(close()));



    aboutAction = new QAction(tr("О программе"), this);

    aboutAction->setShortcut(tr("Ctrl+B"));

    connect(aboutAction, SIGNAL(triggered()),

            this, SLOT(about()));

    //все пока коннектятся к Rect

    //вариант использования(бывший Rect)

	//DiagramItem item(DiagramItem::Step, itemMenu);

	//QIcon icon(item.image());

	this->rectAction = new QAction(QIcon(":/images/usecase.png"),tr("Вариант использования"),this);

	connect(rectAction, SIGNAL(triggered()),

		this, SLOT(on_rectAction()));

    

    //участники



    this->actorAction = new QAction(QIcon(":/images/actor.png"),tr("Участник"),this);

	connect(actorAction, SIGNAL(triggered()),

		this, SLOT(on_actorAction()));

    

    //комментарии



    this->commAction = new QAction(QIcon(":/images/comment.png"),tr("Комментарий"),this);

	connect(commAction, SIGNAL(triggered()),

		this, SLOT(on_commAction()));

    

    //картинка вставляемая



    this->picAction = new QAction(QIcon(":/images/pic.png"),tr("Изображение"),this);

	connect(picAction, SIGNAL(triggered()),

		this, SLOT(on_picAction()));



    //сохранение в картинку



    this->saveToPicAction = new QAction(tr("Сохранить в картинку..."),this);

	connect(saveToPicAction, SIGNAL(triggered()),

		this, SLOT(on_saveToPicAction()));



    //сохранить

    saveAction = new QAction(tr("Сохранить"), this);

    saveAction->setShortcut(tr("Ctrl+S"));

    connect(saveAction, SIGNAL(triggered()),

            this, SLOT(on_saveAction()));

    //сохранить как

    saveAsAction = new QAction(tr("Сохранить как..."), this);

    saveAsAction->setShortcut(tr("Ctrl+Alt+B"));

    connect(saveAsAction, SIGNAL(triggered()),

            this, SLOT(on_saveAsAction()));

    //открыть

    openAction = new QAction(tr("Открыть..."), this);

    openAction->setShortcut(tr("Ctrl+O"));

    connect(openAction, SIGNAL(triggered()),

            this, SLOT(on_openAction()));

    //создать

    createAction = new QAction(tr("Создать"), this);

    createAction->setShortcut(tr("Ctrl+N"));

    connect(createAction, SIGNAL(triggered()),

            this, SLOT(on_createAction()));

}

void MainWindow::on_rectAction()

{

	int id = 0;

	if (id == InsertTextButton)

	{

		scene->setMode(DiagramScene::InsertText);

	}

	else 

	{

		scene->setItemType(DiagramItem::Step);

		scene->setMode(DiagramScene::InsertItem);

	}
        scene->update();

    view->update();

}

void MainWindow::on_actorAction()

{

	int id = 0;

	if (id == InsertTextButton)

	{

		scene->setMode(DiagramScene::InsertActor);

	}

	else 

	{

		scene->setItemType(DiagramItem::Step);

	    scene->setMode(DiagramScene::InsertActor);

	}

    scene->update();

    view->update();

}

void MainWindow::on_commAction()

{

	int id = InsertTextButton;

	if (id == InsertTextButton)

	{

		scene->setMode(DiagramScene::InsertText);

	}

	else 

	{

		scene->setItemType(DiagramItem::Step);

		scene->setMode(DiagramScene::InsertItem);

	}
    scene->update();

    view->update();

}

void MainWindow::on_picAction()

{

    QString filename=QFileDialog::getOpenFileName(this,QString(tr("Открыть файл с изображением")),QString(),QString("Images (*.png);;Все файлы(*.*)"));

   if(QFile::exists(filename))

	{

        scene->setImage(filename);

        scene->imageOnScene();

        scene->update();

        view->update();

    }

}

void MainWindow::on_saveToPicAction()

{

	QString fileName = QFileDialog::getSaveFileName(this,

													tr("Сохранение в картинку"),

													"",

													tr("Images (*.png)"));

	QImage image(scene->width(), scene->height(), QImage::Format_ARGB32_Premultiplied);

	image.fill(NULL);

	QPainter painter(&image);

	scene->render(&painter);

	image.save(fileName);

}

void MainWindow::on_saveAction() {
    QString filename = QFileDialog::getSaveFileName(this, QString("Сохранить файл"), QDir::currentPath(), QString("Use case diagram(*.vox)"));
 
    //check file
    QFile file(filename);
    if(!file.open(QIODevice::WriteOnly)) {
        QMessageBox msgBox;
        msgBox.setText("Не возможно сохранить файл");
        msgBox.exec();
        return;
    }
    
    QDataStream output(&file);

    QMessageBox msgBox;
    msgBox.setText(QString::number(scene->getEllipseItemList().size()));
    msgBox.exec();

    //save ellipses
    output << scene->getEllipseItemList().size();
    for(int i = 0; i < scene->getEllipseItemList().size(); i++) {
        output << scene->getEllipseItemList()[i];
    }

    // output << scene->getLineItemList().size();    
    // for(int i = 0; i < scene->getLineItemList().size(); i++) {
    //     output << scene->getLineItemList()[i];
    // }
        
    // output << scene->getLineItem2List().size();
    // for(int i = 0; i < scene->getLineItem2List().size(); i++) {
    //     output << scene->getLineItem2List()[i];
    // }
  
    //save comments
    output << scene->getTextItemList().size();
    for(int i = 0; i < scene->getTextItemList().size(); i++) {
        output << scene->getTextItemList()[i];
    }
     
    //save actors
    output << scene->getActorItemList().size();
    for(int i = 0; i < scene->getActorItemList().size(); i++) {
         output << scene->getActorItemList()[i];
    }
    
    //save image
    output << 1;
    output << scene->getImageItem()->getImage();
    
    file.close();
}

void MainWindow::on_saveAsAction() {
    on_saveAction();
}

void MainWindow::on_openAction() {
    QString filename = QFileDialog::getOpenFileName(this, QString("Открыть файл"), QDir::currentPath(), QString("Use case diagram(*.vox)"));
    
    //check file
    if(!QFile::exists(filename)) {
        QMessageBox msgBox;
        msgBox.setText(filename);
        msgBox.exec();
        return;
    }
    QFile file(filename);
    if(!file.open(QIODevice::ReadOnly)) {
        QMessageBox msgBox;
        msgBox.setText(filename);
        msgBox.exec();
        return;
    }
    
    QDataStream input(&file);
    int size;
    
    //read ellipses
    input >> size;    
    for(int i = 0; i < size; i++) {
        DiagramEllipseItem * ellipseItem = new DiagramEllipseItem();
        input >> ellipseItem;
        scene->addEllipseItemList(ellipseItem);
        
		ellipseItem->setTextInteractionFlags(Qt::TextEditorInteraction);
        scene->addItem(ellipseItem);
    }
    
    //input >> size;    
        
    // for(int i = 0; i < size; i++) {
    //     QGraphicsLineItem *line = new QGraphicsLineItem();
    //     QLineF lineF;
    //     input >> lineF;
    //     line->setLine(lineF);
    //     scene->addLineItemList(line);
    //     
    //     line->setPen(QPen(Qt::black, 2));
    //     scene->addItem(line);
    // }
    
    //read comments
    input >> size;  
    for(int i = 0; i < size; i++) {
        DiagramTextItem * textItem = new DiagramTextItem();
        input >> textItem;
        scene->addTextItemList(textItem);
        
		textItem->setTextInteractionFlags(Qt::TextEditorInteraction);
        scene->addItem(textItem);
    }
    
    //read actors
    input >> size;  
    for(int i = 0; i < size; i++) {
        DiagramActorItem * actorItem = new DiagramActorItem();
        input >> actorItem;
        scene->addActorItemList(actorItem);
        
        actorItem->setTextWidth(50);
        scene->addItem(actorItem);
    }    
    
    //read image
    input >> size;
    if(size == 1) {
        QImage image;
        input >> image;
        DiagramImageItem * imageItem = new DiagramImageItem(image);
        scene->setImageItem(imageItem);
        
        scene->addItem(imageItem);
    }
    
    file.close();
}

void MainWindow::on_createAction()

{

	

}

//! [24]

void MainWindow::createMenus()

{

    fileMenu = menuBar()->addMenu(tr("&Файл"));

    fileMenu->addAction(createAction);

    fileMenu->addAction(openAction);

    fileMenu->addAction(saveAction);

    fileMenu->addAction(saveAsAction);

    fileMenu->addAction(saveToPicAction);

    fileMenu->addAction(exitAction);



   /* itemMenu = menuBar()->addMenu(tr("&Item"));

    itemMenu->addAction(deleteAction);

    itemMenu->addSeparator();

    itemMenu->addAction(toFrontAction);

    itemMenu->addAction(sendBackAction);*/



    aboutMenu = menuBar()->addMenu(tr("&Помощь"));

    aboutMenu->addAction(aboutAction);

}

//! [24]



//! [25]

void MainWindow::createToolbars()

{

//! [25]



    QToolButton *pointerButton = new QToolButton;

    pointerButton->setCheckable(true);

    pointerButton->setChecked(true);

    pointerButton->setIcon(QIcon(":/images/pointer.png"));

    

    QToolButton *linePointerButton = new QToolButton;

    linePointerButton->setCheckable(true);

    linePointerButton->setIcon(QIcon(":/images/linepointer.png"));

    QToolButton *linePointerGeneralButton = new QToolButton;

    linePointerGeneralButton->setCheckable(true);

    linePointerGeneralButton->setIcon(QIcon(":/images/line2pointer.png"));
    
    QToolButton *linePointerDottedButton = new QToolButton;

    linePointerDottedButton->setCheckable(true);

    linePointerDottedButton->setIcon(QIcon(":/images/linedottedpointer.png"));



    pointerTypeGroup = new QButtonGroup(this);

    pointerTypeGroup->addButton(pointerButton, int(DiagramScene::MoveItem));

    pointerTypeGroup->addButton(linePointerButton,

                                int(DiagramScene::InsertLine));
    pointerTypeGroup->addButton(linePointerGeneralButton,

                                int(DiagramScene::InsertLineGeneral));
    pointerTypeGroup->addButton(linePointerDottedButton,

                                int(DiagramScene::InsertLineDotted));

    connect(pointerTypeGroup, SIGNAL(buttonClicked(int)),

            this, SLOT(pointerGroupClicked(int)));



    sceneScaleCombo = new QComboBox;

    QStringList scales;

    scales << tr("50%") << tr("100%") << tr("150%") << tr("200%");

    sceneScaleCombo->addItems(scales);

    sceneScaleCombo->setCurrentIndex(1);

    connect(sceneScaleCombo, SIGNAL(currentIndexChanged(QString)),

            this, SLOT(sceneScaleChanged(QString)));







    editToolBar = addToolBar(tr("Редактирование"));

    editToolBar->addWidget(pointerButton);

    editToolBar->addWidget(linePointerButton);
    editToolBar->addWidget(linePointerGeneralButton);
    editToolBar->addWidget(linePointerDottedButton);

    editToolBar->addAction(deleteAction);

    editToolBar->addAction(this->rectAction);

    editToolBar->addAction(this->actorAction);

    editToolBar->addAction(this->commAction);

    editToolBar->addAction(this->picAction);

    editToolBar->addWidget(sceneScaleCombo);

	

    fontColorToolButton = new QToolButton;

    fontColorToolButton->setPopupMode(QToolButton::MenuButtonPopup);

    fontColorToolButton->setMenu(createColorMenu(SLOT(textColorChanged()),

                                                 Qt::black));

}

//! [27]



//! [28]

QWidget *MainWindow::createBackgroundCellWidget(const QString &text,

                        const QString &image)

{

    QToolButton *button = new QToolButton;

    button->setText(text);

    button->setIcon(QIcon(image));

    button->setIconSize(QSize(50, 50));

    button->setCheckable(true);

    backgroundButtonGroup->addButton(button);



    QGridLayout *layout = new QGridLayout;

    layout->addWidget(button, 0, 0, Qt::AlignHCenter);

    layout->addWidget(new QLabel(text), 1, 0, Qt::AlignCenter);



    QWidget *widget = new QWidget;

    widget->setLayout(layout);



    return widget;

}

//! [28]



//! [29]

QWidget *MainWindow::createCellWidget(const QString &text,

                      DiagramItem::DiagramType type)

{



    DiagramItem item(type, itemMenu);

    QIcon icon(item.image());



    QToolButton *button = new QToolButton;

    button->setIcon(icon);

    button->setIconSize(QSize(50, 50));

    button->setCheckable(true);

    buttonGroup->addButton(button, int(type));



    QGridLayout *layout = new QGridLayout;

    layout->addWidget(button, 0, 0, Qt::AlignHCenter);

    layout->addWidget(new QLabel(text), 1, 0, Qt::AlignCenter);



    QWidget *widget = new QWidget;

    widget->setLayout(layout);



    return widget;

}

//! [29]



//! [30]

QMenu *MainWindow::createColorMenu(const char *slot, QColor defaultColor)

{

    QList<QColor> colors;

    colors << Qt::black << Qt::white << Qt::red << Qt::blue << Qt::yellow;

    QStringList names;

    names << tr("black") << tr("white") << tr("red") << tr("blue")

          << tr("yellow");



    QMenu *colorMenu = new QMenu(this);

    for (int i = 0; i < colors.count(); ++i) {

        QAction *action = new QAction(names.at(i), this);

        action->setData(colors.at(i));

        action->setIcon(createColorIcon(colors.at(i)));

        connect(action, SIGNAL(triggered()),

                this, slot);

        colorMenu->addAction(action);

        if (colors.at(i) == defaultColor) {

            colorMenu->setDefaultAction(action);

        }

    }

    return colorMenu;

}

//! [30]



//! [31]

QIcon MainWindow::createColorToolButtonIcon(const QString &imageFile,

                        QColor color)

{

    QPixmap pixmap(50, 80);

    pixmap.fill(Qt::transparent);

    QPainter painter(&pixmap);

    QPixmap image(imageFile);

    QRect target(0, 0, 50, 60);

    QRect source(0, 0, 42, 42);

    painter.fillRect(QRect(0, 60, 50, 80), color);

    painter.drawPixmap(target, image, source);



    return QIcon(pixmap);

}

//! [31]



//! [32]

QIcon MainWindow::createColorIcon(QColor color)

{

    QPixmap pixmap(20, 20);

    QPainter painter(&pixmap);

    painter.setPen(Qt::NoPen);

    painter.fillRect(QRect(0, 0, 20, 20), color);



    return QIcon(pixmap);

}

