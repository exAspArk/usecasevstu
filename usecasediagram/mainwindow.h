#ifndef MAINWINDOW_H

#define MAINWINDOW_H



#include <QMainWindow>
#include <QFileDialog>
#include "diagramitem.h"
#include "diagramscene.h"

QT_BEGIN_NAMESPACE

class QAction;

class QToolBox;

class QSpinBox;

class QComboBox;

class QFontComboBox;

class QButtonGroup;

class QLineEdit;

class QGraphicsTextItem;

class QFont;

class QToolButton;

class QAbstractButton;

class QGraphicsView;

QT_END_NAMESPACE



//! [0]

class MainWindow : public QMainWindow

{

    Q_OBJECT



public:
   MainWindow();
   bool isEnded(){
       return isEnd;
   }
   void clearScene() {
       scene->clear();
       scene->clearData();
   }
   
private slots:

    void buttonGroupClicked(int id);

    void deleteItem();

    void pointerGroupClicked(int id);

    void bringToFront();

    void sendToBack();

    void itemInserted(DiagramItem *item);

    void textInserted(QGraphicsTextItem *item);

    void currentFontChanged(const QFont &font);

    void fontSizeChanged(const QString &size);

    void sceneScaleChanged(const QString &scale);

    void textButtonTriggered();

    void fillButtonTriggered();

    void lineButtonTriggered();

    void handleFontChange();

    void itemSelected(QGraphicsItem *item);

    void about();

    //

	void on_rectAction();

    void on_actorAction();

    void on_commAction();

    void on_picAction();

    void on_saveToPicAction();

    void on_saveAction();

    void on_saveAsAction();

    void on_openAction();

    void on_createAction();



private:
    bool isEnd;
    QString filename;
    void closeEvent(QCloseEvent * event);
    void createToolBox();

    void createActions();

    void createMenus();

    void createToolbars();

    QWidget *createBackgroundCellWidget(const QString &text,

                                        const QString &image);

    QWidget *createCellWidget(const QString &text,

                              DiagramItem::DiagramType type);

    QMenu *createColorMenu(const char *slot, QColor defaultColor);

    QIcon createColorToolButtonIcon(const QString &image, QColor color);

    QIcon createColorIcon(QColor color);



    DiagramScene *scene;

    QGraphicsView *view;



    QAction *exitAction;

    QAction *addAction;

    QAction *deleteAction;



    QAction *toFrontAction;

    QAction *sendBackAction;

    QAction *aboutAction;



    QMenu *fileMenu;

    QMenu *itemMenu;

    QMenu *aboutMenu;



    QToolBar *textToolBar;

    QToolBar *editToolBar;

    QToolBar *colorToolBar;

    QToolBar *pointerToolbar;



    QComboBox *sceneScaleCombo;

    QComboBox *itemColorCombo;

    QComboBox *textColorCombo;

    QComboBox *fontSizeCombo;

    QFontComboBox *fontCombo;



    QToolBox *toolBox;

    QButtonGroup *buttonGroup;

    QButtonGroup *pointerTypeGroup;

    QButtonGroup *backgroundButtonGroup;

    QToolButton *fontColorToolButton;

    QToolButton *fillColorToolButton;

    QToolButton *lineColorToolButton;

    QAction *boldAction;

    QAction *underlineAction;

    QAction *italicAction;

    QAction *textAction;

    QAction *fillAction;

    QAction *lineAction;

	

    

    QAction *rectAction;//вариант использования(овал)

    QAction *actorAction;//участник(человечек)

    QAction *commAction;//комментарий

    QAction *picAction;//картинка вставляемая

    QAction *saveToPicAction;//сохранение в картинку

    QAction *saveAction;//сохраненить

    QAction *saveAsAction;//сохраненить как

    QAction *openAction;//открыть

    QAction *createAction;//создать



};

//! [0]



#endif

