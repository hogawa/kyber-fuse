CC       = gcc
CFLAGS   = -Wall -g -O2 -Wno-unused-function
INCLUDES = -I ../output/
VPATH    = ../output/
OBJS     = kyber_fused.o

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $^ -o $(@F)

all: kyber_kem_test

kyber_kem_test: $(OBJS) kyber_kem_test.o
	$(CC) $(OBJS) kyber_kem_test.o -o kyber_kem_test

clean:
	rm -rf *.o kyber_kem_test
