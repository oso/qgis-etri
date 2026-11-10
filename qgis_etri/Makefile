TARGETS := $(RSFILES)

all: $(TARGETS)

ui/resources_rc.py: ui/resources.qrc
	pyrcc5 -o $@ $<

mrproper:
	rm -f $(TARGETS)

.PHONY: all mrproper
