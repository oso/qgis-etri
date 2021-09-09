TARGETS := $(UIFILES:%.ui=%.py) $(RSFILES)

all: $(TARGETS)

ui/resources_rc.py: ui/resources.qrc
	pyrcc5 -o $@ $<

ui/%.py: ui/%.ui
	pyuic5 --import-from=qgis_etri.ui -o $@ $<

mrproper:
	rm -f $(TARGETS)

.PHONY: all mrproper
