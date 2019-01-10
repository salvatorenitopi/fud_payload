CC ?= gcc
STRIP ?= strip
# STRIPFLAGS += -sx
CFLAGS += -Wall -Os 
# CFLAGS += -DDEBUG=1
# CFLAGS += -static
CFLAGS64 += -fPIC 
OUT ?= payload

32:
	$(CC) payload.c -o $(OUT) $(CFLAGS)
	$(STRIP) $(STRIPFLAGS) $(OUT)

64:
	$(CC) payload.c $(CFLAGS64) -o $(OUT) $(CFLAGS)
	$(STRIP) $(STRIPFLAGS) $(OUT)