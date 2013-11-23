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
PKG_FILES +=	$(RSFILES:%.ui=%.py)

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
	rm -f mcda/*.pyc
	rm -f tests/*.pyc
	rm -f ui/*.pyc
	rm -f *.pyc

mrproper: clean
	rm -f $(TARGETS)

zip: $(TARGETS)
	@ln -sf . qgis_etri
	zip -9v qgis_etri.zip $(PKG_FILES:%=qgis_etri/%)
	@rm qgis_etri

.PHONY: all clean mrproper zip
