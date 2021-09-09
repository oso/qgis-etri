RSFILES :=	ui/resources_rc.py

UIFILES :=	ui/main_window.ui
UIFILES +=	ui/inference_results.ui

PKG_FILES +=	metadata.txt
PKG_FILES +=	__init__.py
PKG_FILES +=	etri_plugin.py
PKG_FILES +=	graphic.py
PKG_FILES +=	layer.py
PKG_FILES +=	main.py
PKG_FILES +=	qgis_utils.py
PKG_FILES +=	table.py
PKG_FILES +=	ui_utils.py
PKG_FILES +=	xmcda.py

PKG_FILES +=	mcda/__init__.py
PKG_FILES +=	mcda/electre_tri.py
PKG_FILES +=	mcda/generate.py
PKG_FILES +=	mcda/types.py

PKG_FILES +=	ui/__init__.py
PKG_FILES +=	$(UIFILES:%.ui=%.py)
PKG_FILES +=	$(RSFILES)

PKG_FILES +=	pysimplesoap/__init__.py
PKG_FILES +=	pysimplesoap/client.py
PKG_FILES +=	pysimplesoap/simplexml.py

PKG_FILES +=	COPYING
PKG_FILES +=	README

QGISDIR ?= .local/share/QGIS/QGIS3/profiles/default
PLUGINNAME = qgis_etri

MAKE_SUBDIR = $(MAKE) -C qgis_etri -e RSFILES="$(RSFILES)" -e UIFILES="$(UIFILES)"

all:
	$(MAKE_SUBDIR) all

clean:
	find . -name '*.pyc' -exec rm --force {} +

mrproper: clean
	$(MAKE_SUBDIR) mrproper

zip: all
	zip -9v $(PLUGINNAME).zip $(PKG_FILES:%=qgis_etri/%)

link: uninstall
	ln -s $(shell pwd)/$(PLUGINNAME) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

unlink: uninstall

install: zip uninstall
	unzip $(PLUGINNAME).zip -d $(HOME)/$(QGISDIR)/python/plugins/

uninstall:
	rm -Rf $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

.PHONY: all clean mrproper zip
