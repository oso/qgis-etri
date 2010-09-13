all: resources.py mainwindow_ui.py 

resources.py: resources.qrc
	pyrcc4 -o resources.py resources.qrc

mainwindow_ui.py: mainwindow.ui
	pyuic4 -o mainwindow_ui.py mainwindow.ui

clean: 
	rm -f *.pyc

.PHONY: all clean
