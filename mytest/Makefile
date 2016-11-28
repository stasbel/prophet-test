FILE=square-bug
SRC_DIR=/home/prophet/prophet-gpl/prophet-test/mytest
TEST_DIR=$(SRC_DIR)/tests

all: clean compile

compile:
	gcc -c $(FILE).c -o $(FILE).o
	gcc $(FILE).o -o $(FILE)

prereq:
	cd tests && make && cd .. && make
	./square-test.py $(SRC_DIR) $(TEST_DIR) $(SRC_DIR)

clean:
	rm -rf $(FILE) $(FILE).o
