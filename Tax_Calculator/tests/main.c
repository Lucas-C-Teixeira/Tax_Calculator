#include <stdio.h>
#include "irpj.h" // Certifique-se que o caminho está correto
#include "iof.h"

void test_irpj() {
    printf("--- Testando IRPJ ---\n");
    // Teste 1: Lucro Real (50k receita - 10k despesa = 40k base)
    // Cálculo: (40k * 0.15) + (20k excedente * 0.10) = 6000 + 2000 = 8000
    Company c1 = {REAL_PROFIT, 50000.0, 10000.0, 0.0};
    double res_irpj = 0.0;
    
    if (calculate_irpj(c1, &res_irpj) == SUCCESS) {
        printf("IRPJ Lucro Real: R$ %.2f (Esperado: 8000.00)\n", res_irpj);
    }

    // Teste 2: Regime Inválido
    Company c2 = {99, 1000.0, 0.0, 0.0};
    if (calculate_irpj(c2, &res_irpj) == ERR_INVALID_REGIME) {
        printf("Erro de regime detectado corretamente.\n\n");
    }
}

void test_iof() {
    printf("--- Testando IOF ---\n");
    // Teste: Crédito PJ (10k por 30 dias)
    IOFRequest req = {IOF_CREDITO_PJ, 10000.0, 30};
    double res_iof = 0.0;

    if (calculate_iof(req, &res_iof) == SUCCESS) {
        printf("IOF Crédito: R$ %.2f\n\n", res_iof);
    }
}

int main(void) {
    test_irpj();
    test_iof();
    return 0;
}