PKG_FILES +=	qgis_etri/metadata.txt
PKG_FILES +=	qgis_etri/__init__.py
PKG_FILES +=	qgis_etri/etri_plugin.py
PKG_FILES +=	qgis_etri/graphic.py
PKG_FILES +=	qgis_etri/layer.py
PKG_FILES +=	qgis_etri/main.py
PKG_FILES +=	qgis_etri/qgis_utils.py
PKG_FILES +=	qgis_etri/table.py

PKG_FILES +=	qgis_etri/mcda/__init__.py
PKG_FILES +=	qgis_etri/mcda/electre_tri.py
PKG_FILES +=	qgis_etri/mcda/generate.py
PKG_FILES +=	qgis_etri/mcda/types.py

PKG_FILES +=	qgis_etri/ui/__init__.py
PKG_FILES +=	qgis_etri/ui/main_window.ui

PKG_FILES +=	qgis_etri/images/etri.png
PKG_FILES +=	qgis_etri/images/etri.svg
PKG_FILES +=	qgis_etri/images/min.svg
PKG_FILES +=	qgis_etri/images/plus.svg

PKG_FILES +=	LICENSE
PKG_FILES +=	README

QGISDIR ?= .local/share/QGIS/QGIS3/profiles/default
PLUGINNAME = qgis_etri

all: zip

clean:
	find . -name '*.pyc' -exec rm --force {} +

mrproper: clean
	rm -f $(PLUGINNAME).zip

zip:
	rm -f $(PLUGINNAME).zip
	zip -9v $(PLUGINNAME).zip $(PKG_FILES)

link: uninstall
	ln -s $(shell pwd)/$(PLUGINNAME) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

unlink: uninstall

install: zip uninstall
	unzip $(PLUGINNAME).zip -d $(HOME)/$(QGISDIR)/python/plugins/

uninstall:
	rm -Rf $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

test:
	python -m pytest

.PHONY: all clean mrproper zip link unlink install uninstall test
