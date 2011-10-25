HEADERS	    =   mainwindow.h \
		diagramitem.h \
		diagramscene.h \
		arrow.h \
		diagramtextitem.h \
    diagramellipseitem.h \
    declarationdatatypes.h \
    diagramimageitem.h \
    diagramactorimageitem.h \
    diagramactorimageitem.h
SOURCES	    =   mainwindow.cpp \
		diagramitem.cpp \
		main.cpp \
		arrow.cpp \
		diagramtextitem.cpp \
		diagramscene.cpp \
    diagramellipseitem.cpp \
    diagramimageitem.cpp \
    diagramactorimageitem.cpp
RESOURCES   =	diagramscene.qrc


# install
target.path = $$[QT_INSTALL_EXAMPLES]/graphicsview/diagramscene
sources.files = $$SOURCES $$HEADERS $$RESOURCES $$FORMS diagramscene.pro images
sources.path = $$[QT_INSTALL_EXAMPLES]/graphicsview/diagramscene
INSTALLS += target sources

symbian: include($$QT_SOURCE_TREE/examples/symbianpkgrules.pri)








