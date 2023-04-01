CC       = gcc
CFLAGS   = -Wall -g -O2 -Wno-unused-function
INCLUDES = -I ../output/ -I ../kyber/ref/
VPATH    = ../output/ ../kyber/ref/
OBJS     = aes256ctr.o fips202.o sha256.o sha512.o randombytes.o kyber_fused.o

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $^ -o $(@F)

all: kyber_kem_test

kyber_kem_test: $(OBJS) kyber_kem_test.o
	$(CC) $(OBJS) kyber_kem_test.o -o kyber_kem_test

clean:
	rm -rf *.o kyber_kem_test
