all: square

square:
	src/run -b src/square-bug.c --full-search tests/square/

clean:
	rm -rf workdir/
