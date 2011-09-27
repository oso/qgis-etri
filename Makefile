RSFILES :=	ui/resources_rc.py

UIFILES :=	ui/etrimain.ui
UIFILES +=	ui/main_window.ui
UIFILES +=	ui/refsdialog.ui
UIFILES +=	ui/infdialog.ui
UIFILES +=	ui/pwdialog.ui

PKG_FILES :=	etrimain.py
PKG_FILES +=	__init__.py
PKG_FILES +=	etri_plugin.py
PKG_FILES +=	pwdialog.py
PKG_FILES +=	ui_utils.py
PKG_FILES +=	etri.py
PKG_FILES +=	qgis_utils.py
PKG_FILES +=	xmcda.py
PKG_FILES +=	infdialog.py
PKG_FILES +=	refsdialog.py

PKG_FILES +=	ui/__init__.py
PKG_FILES +=	ui/etrimain.py
PKG_FILES +=	ui/refsdialog.py
PKG_FILES +=	ui/infdialog.py
PKG_FILES +=	ui/pwdialog.py
PKG_FILES +=	ui/resources_rc.py

PKG_FILES +=	pysimplesoap/__init__.py
PKG_FILES +=	pysimplesoap/client.py
PKG_FILES +=	pysimplesoap/simplexml.py

PKG_FILES +=	COPYING
PKG_FILES +=	README

TARGETS := $(UIFILES:%.ui=%.py) $(RSFILES)

all: $(TARGETS) 

ui/resources_rc.py: ui/resources.qrc
	pyrcc4 -o $@ $<

ui/%.py: ui/%.ui 
	pyuic4 -o $@ $<

clean: 
	rm -f pysimplesoap/*.pyc
	rm -f ui/*.pyc
	rm -f mcda/*.pyc
	rm -f *.pyc

mrproper: clean
	rm -f $(TARGETS)

zip: $(TARGETS)
	@ln -sf . qgis_etri
	zip -9v qgis_etri.zip $(PKG_FILES:%=qgis_etri/%)
	@rm qgis_etri

.PHONY: all clean mrproper zip
