TARGETS := resources.py Ui_etridialog.py

all: $(TARGETS) 

resources.py: resources.qrc
	pyrcc4 -o resources.py resources.qrc

Ui_etridialog.py: etridialog.ui
	pyuic4 -o $@ $<

clean: 
	rm -f *.pyc

mrproper: clean
	rm -f $(TARGETS)

.PHONY: all clean mrproper
