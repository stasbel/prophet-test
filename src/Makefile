PROPHET=/home/ubuntu/Workspace/prophet/src/prophet
PARA=/home/ubuntu/Workspace/prophet/crawler/para-all.out
CONF=repair.conf
WORKDIR=workdir
FULLSEARCHFLAGS=
SUMFILE=summary
LOGFILE=log
EXTRAFLAGS=
FLAGS=$(FULLSEARCHFLAGS) -ll=10 -vl=10 -no-clean-up -stats -summary-file=$(SUMFILE) -log=$(LOGFILE) $(EXTRAFLAGS)

all: fix

help:
	$(PROPHET) --help

init:
	$(PROPHET) $(CONF) -r $(WORKDIR) -init-only $(FLAGS)

fix:
	$(PROPHET) -feature-para $(PARA) -r $(WORKDIR) -skip-verify $(FLAGS)
