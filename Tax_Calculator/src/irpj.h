#ifndef IRPJ_H
#define IRPJ_H

// Regimes
typedef enum {
    REAL_PROFIT = 1,
    PRESUMED_PROFIT = 2
} TaxRegime;

// Error codes
#define SUCCESS 0
#define ERR_INVALID_REGIME -1
#define ERR_INVALID_MARGIN -2
#define ERR_INVALID_INPUT -3
#define ERR_NULL_POINTER -4

typedef struct {
    TaxRegime regime;
    double revenue;
    double expenses;
    double margin;
} Company;

/**
 * Calculates IRPJ tax
 */
int calculate_irpj(Company c, double *irpj);

#endif