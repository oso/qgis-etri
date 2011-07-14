TARGETS :=	resources_rc.py
TARGETS +=	Ui_etrimain.py
TARGETS +=	Ui_refsdialog.py
TARGETS +=	Ui_infdialog.py
TARGETS +=	Ui_pwdialog.py

PKG_FILES :=	etrimain.py
PKG_FILES +=	__init__.py
PKG_FILES +=	resources_rc.py
PKG_FILES +=	Ui_refsdialog.py
PKG_FILES +=	etri_plugin.py
PKG_FILES +=	pwdialog.py
PKG_FILES +=	Ui_etrimain.py
PKG_FILES +=	ui_utils.py
PKG_FILES +=	etri.py
PKG_FILES +=	qgis_utils.py
PKG_FILES +=	Ui_infdialog.py
PKG_FILES +=	xmcda.py
PKG_FILES +=	infdialog.py
PKG_FILES +=	refsdialog.py
PKG_FILES +=	Ui_pwdialog.py
PKG_FILES +=	pysimplesoap/client.py
PKG_FILES +=	pysimplesoap/simplexml.py
PKG_FILES +=	COPYING
PKG_FILES +=	README

all: $(TARGETS) 

resources_rc.py: resources.qrc
	pyrcc4 -o resources_rc.py resources.qrc

Ui_pwdialog.py: pwdialog.ui
	pyuic4 -o $@ $<

Ui_infdialog.py: infdialog.ui
	pyuic4 -o $@ $<

Ui_refsdialog.py: refsdialog.ui
	pyuic4 -o $@ $<

Ui_etrimain.py: etrimain.ui
	pyuic4 -o $@ $<

clean: 
	rm -f *.pyc

mrproper: clean
	rm -f $(TARGETS)

zip:
	@ln -sf . qgis_etri
	zip -9v qgis_etri.zip $(PKG_FILES:%=qgis_etri/%)
	@rm qgis_etri

.PHONY: all clean mrproper zip
