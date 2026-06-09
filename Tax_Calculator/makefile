CC = gcc
CFLAGS = -Wall -Wextra -Werror -Isrc
LDFLAGS = -shared

TARGET = bin/libtaxes.dll
SRCS = src/irpf.c src/irpj.c src/iof.c
OBJS = src/irpf.o src/irpj.o src/iof.o

all: setup $(TARGET)

setup:
	mkdir -p bin

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $(TARGET) $(OBJS)

src/%.o: src/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f src/*.o bin/*.dll

.PHONY: all setup clean