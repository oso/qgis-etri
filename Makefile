UIFILES :=	ui/main_window.ui

PKG_FILES +=	metadata.txt
PKG_FILES +=	__init__.py
PKG_FILES +=	etri_plugin.py
PKG_FILES +=	graphic.py
PKG_FILES +=	layer.py
PKG_FILES +=	main.py
PKG_FILES +=	qgis_utils.py
PKG_FILES +=	table.py

PKG_FILES +=	mcda/__init__.py
PKG_FILES +=	mcda/electre_tri.py
PKG_FILES +=	mcda/generate.py
PKG_FILES +=	mcda/types.py

PKG_FILES +=	ui/__init__.py
PKG_FILES +=	$(UIFILES)

PKG_FILES +=	images/etri.png
PKG_FILES +=	images/etri.svg
PKG_FILES +=	images/min.svg
PKG_FILES +=	images/plus.svg

PKG_FILES +=	COPYING
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
	zip -9v $(PLUGINNAME).zip $(PKG_FILES:%=qgis_etri/%)

link: uninstall
	ln -s $(shell pwd)/$(PLUGINNAME) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

unlink: uninstall

install: zip uninstall
	unzip $(PLUGINNAME).zip -d $(HOME)/$(QGISDIR)/python/plugins/

uninstall:
	rm -Rf $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

.PHONY: all clean mrproper zip link unlink install uninstall
