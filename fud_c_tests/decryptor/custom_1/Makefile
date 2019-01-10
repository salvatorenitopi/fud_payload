# https://gist.github.com/giuscri/4bfbdc160dd0741341fa5c596f92e227

.PHONY: all memtest clean
CC=gcc
CFLAGS=-Wall -g -O0 -m32
CFLAGS += -DDEBUG=1

all: AES

AES: AES.o
	$(CC) $(CFLAGS) -o $@ $^ -lcrypto

memtest: AES
	@echo -n 'YELLOW SUBMARINE'|valgrind -q ./AES 1> /dev/null && \
		echo '*** [+1] NO memory mess.'

clean:
	rm -rf AES *.o
