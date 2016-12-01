SUBDIRS=src tests

all: build

build:
	make -C src

clean:
	for dir in $(SUBDIRS) ; do \
		make -C $$dir clean ; \
	done
