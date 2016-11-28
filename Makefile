PROPHET=/home/prophet/prophet-gpl/src/prophet
FEATURE=-feature-para /home/prophet/prophet-gpl/crawler/para-all.out
CONF=/home/prophet/prophet-gpl/prophet-test/mytest/square.conf
LOCFILE=location
LOGFILE=log
SUMFILE=summary
FIXFILE=fix
FULLSEARCHFLAGS=-consider-all -full-explore -full-synthesis -cond-ext
FLAGS=$(FULLSEARCHFLAGS) -ll=10 -vl=10 -no-clean-up -stats -summary-file=$(SUMFILE) -print-fix-only=$(FIXFILE)
WORKDIR=tmp

all: run

help:
	$(PROPHET) --help

init:
	$(PROPHET) $(CONF) -r $(WORKDIR) -init-only

run:
	touch Makefile
	$(PROPHET) $(FEATURE) -r $(WORKDIR) -skip-verify $(FLAGS)

clean:
	rm -rf __* repair.log $(LOCFILE) $(LOGFILE) $(SUMFILE) $(FIXFILE) $(WORKDIR)/ square-fixsquare-bug.c*
