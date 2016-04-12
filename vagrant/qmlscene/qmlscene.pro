CONFIG      += plugin release warn_on
QT          += qml

# Work around QTBUG-39300.
CONFIG -= android_install

TARGET      = pyqt5qmlplugin
TEMPLATE    = lib

INCLUDEPATH += /usr/include/python3.4m /usr/include/python3.4m
LIBS        += -L/usr/lib/x86_64-linux-gnu -lpython3.4m

SOURCES     = pluginloader.cpp
HEADERS     = pluginloader.h

# Install.
target.path = /usr/lib/x86_64-linux-gnu/qt5/plugins/PyQt5

python.path = /usr/lib/x86_64-linux-gnu/qt5/plugins/PyQt5
python.files = python

INSTALLS    += target python

INCLUDEPATH += /home/vagrant/CSV-Tools/vagrant/PyQt-gpl-5.5.1/qmlscene
VPATH = /home/vagrant/CSV-Tools/vagrant/PyQt-gpl-5.5.1/qmlscene

