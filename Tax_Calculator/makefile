# O compilador
CC = gcc
CFLAGS = -Wall -Wextra

# Pastas (Ajustado para a sua estrutura)
SRC_DIR = FinalProjec/src
OBJ_DIR = FinalProjec/bin
TEST_DIR = FinalProjec/tests

# Encontrar todos os arquivos .c
SRC = $(wildcard $(SRC_DIR)/*.c)
# Mapear .c para .o dentro da pasta bin
OBJ = $(patsubst $(SRC_DIR)/%.c, $(OBJ_DIR)/%.o, $(SRC))

# Executável
EXEC = calculadora.exe

# Regra principal
all: $(EXEC)

$(EXEC): $(OBJ) $(TEST_DIR)/main.c
	$(CC) $(CFLAGS) $(TEST_DIR)/main.c $(OBJ) -o $(EXEC)

# Regra para compilar cada .c em .o
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ_DIR)/*.o $(EXEC)